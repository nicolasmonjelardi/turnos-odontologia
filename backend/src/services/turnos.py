"""Service crear_turno — change c-03. Router thin; acá vive la transacción.

Flujo: resuelve duración por prestación → precheck `valida()` (409 amable) →
persiste `reservado` + auditoría con commit/rollback. `IntegrityError` del
EXCLUDE (race del precheck, solo vía PG) se revalida contra el estado fresco
para identificar el conflicto real; si no se identifica, se reporta 409 por
nombre de constraint sin turno identificado (nunca se fabrica uno).
"""

import secrets
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from domain.agenda import (
    FechaInvalida,
    NuevoTurno,
    TurnoExistente,
    valida,
)
from repos import InMemoryAgendaStore, InMemoryUoW, TurnoData


class ExclusionRaceError(ValueError):
    """EXCLUDE disparó pero el conflicto ya no es visible: 409 por constraint."""

    def __init__(self, codigo: str) -> None:
        super().__init__(codigo)
        self.codigo = codigo


def _existentes(store: InMemoryAgendaStore) -> list[TurnoExistente]:
    return [
        TurnoExistente(id=t.id, profesional_id=t.profesional_id, sillon_id=t.sillon_id,
                       inicio=t.inicio, fin=t.fin)
        for t in store.turnos if t.estado != "cancelado"
    ]


def _codigo_por_constraint(msg: str) -> str:
    return "SILLON_OCUPADO" if "ex_turnos_no_solape_sillon" in msg else "PROFESIONAL_OCUPADO"


async def crear_turno(*, store: InMemoryAgendaStore, profesional_id: int, sillon_id: int,
                      prestacion_id: int, paciente_id: int, inicio: datetime,
                      actor: str = "stub-recepcionista") -> TurnoData:
    try:
        duracion_min = store.prestaciones[prestacion_id]
    except KeyError:
        raise FechaInvalida(f"prestacion_id desconocido: {prestacion_id}") from None
    nuevo = NuevoTurno(profesional_id=profesional_id, sillon_id=sillon_id,
                       inicio=inicio, duracion_min=duracion_min)
    fin = valida(nuevo, _existentes(store))  # precheck: 409 amable (no decide)
    async with InMemoryUoW(store) as uow:
        turno = await uow.turnos.crear(
            profesional_id=profesional_id, sillon_id=sillon_id, prestacion_id=prestacion_id,
            paciente_id=paciente_id, inicio=inicio, fin=fin, estado="reservado",
            token_publico=secrets.token_urlsafe(16),
        )
        await uow.auditoria.registrar(turno_id=turno.id, accion="crear", actor=actor)
        try:
            await uow.commit()
        except IntegrityError as e:
            # La verdad la dice el EXCLUDE: revalida en fresco para identificar
            # el turno ganador de la race; si ya no es visible, 409 por constraint.
            await uow.rollback()
            valida(nuevo, _existentes(store))  # relanza SolapamientoError si sigue visible
            raise ExclusionRaceError(_codigo_por_constraint(str(e))) from e
    return turno
