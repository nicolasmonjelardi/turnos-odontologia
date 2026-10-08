"""RED task 3.3: repos async + UnitOfWork (commit/rollback en una transacción).

Implementación en memoria como doble del PG (el PG real es opt-in):
commit persiste turno + auditoría juntos; rollback no persiste nada.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

AR = ZoneInfo("America/Argentina/Buenos_Aires")


def _inicio():
    return datetime(2026, 10, 15, 10, 0, tzinfo=AR)


async def test_uow_commit_persiste_turno_y_auditoria_juntos():
    from repos import InMemoryUoW, seed_ficticio

    store = seed_ficticio()
    async with InMemoryUoW(store) as uow:
        turno = await uow.turnos.crear(
            profesional_id=1, sillon_id=1, prestacion_id=1, paciente_id=1,
            inicio=_inicio(), fin=_inicio().replace(hour=10, minute=30),
            estado="reservado", token_publico="tok-1",
        )
        await uow.auditoria.registrar(turno_id=turno.id, accion="crear", actor="stub")
        await uow.commit()
    assert len(store.turnos) == 5  # 4 del seed + 1
    assert any(a.turno_id == turno.id and a.accion == "crear" for a in store.auditoria)


async def test_uow_rollback_no_persiste_nada():
    from repos import InMemoryUoW, seed_ficticio

    store = seed_ficticio()
    try:
        async with InMemoryUoW(store) as uow:
            turno = await uow.turnos.crear(
                profesional_id=1, sillon_id=1, prestacion_id=1, paciente_id=1,
                inicio=_inicio(), fin=_inicio().replace(hour=10, minute=30),
                estado="reservado", token_publico="tok-x",
            )
            await uow.auditoria.registrar(turno_id=turno.id, accion="crear", actor="stub")
            raise RuntimeError("falla antes del commit")
    except RuntimeError:
        pass
    assert len(store.turnos) == 4
    assert store.auditoria == []


async def test_seed_ficticio_sin_choques_y_con_contenido_minimo():
    from domain.agenda import NuevoTurno, TurnoExistente, valida
    from repos import seed_ficticio

    store = seed_ficticio()
    assert len(store.profesionales) == 2
    assert len(store.sillones) == 2
    assert len(store.prestaciones) == 5
    assert len(store.pacientes) == 3
    assert len(store.turnos) == 4
    # cada turno del seed es válido contra los anteriores (sin choques)
    vistos: list[TurnoExistente] = []
    for t in store.turnos:
        minutos = int((t.fin - t.inicio).total_seconds() // 60)
        valida(
            NuevoTurno(profesional_id=t.profesional_id, sillon_id=t.sillon_id,
                       inicio=t.inicio, duracion_min=minutos),
            vistos,
        )
        vistos.append(TurnoExistente(id=t.id, profesional_id=t.profesional_id,
                                     sillon_id=t.sillon_id, inicio=t.inicio, fin=t.fin))
