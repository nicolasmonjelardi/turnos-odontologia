"""Repos + UnitOfWork — change c-03.

Doble en memoria del PG (`InMemoryAgendaStore` + `InMemoryUoW`) para que la
suite corra sin infra externa. El PG real (modelos + EXCLUDE) es opt-in
con TEST_PG=1. `seed_ficticio()` refleja `seed_ficticio.sql` (datos FICTICIOS).
"""

from dataclasses import dataclass, field
from datetime import datetime
from types import TracebackType
from typing import Self
from zoneinfo import ZoneInfo

AR = ZoneInfo("America/Argentina/Buenos_Aires")


@dataclass
class TurnoData:
    id: int
    profesional_id: int
    sillon_id: int
    prestacion_id: int
    paciente_id: int
    inicio: datetime
    fin: datetime
    estado: str = "reservado"
    origen: str = "recepcion"
    token_publico: str = ""


@dataclass
class AuditoriaData:
    id: int
    turno_id: int
    accion: str
    actor: str


@dataclass
class InMemoryAgendaStore:
    profesionales: dict[int, str] = field(default_factory=dict)
    sillones: dict[int, str] = field(default_factory=dict)
    prestaciones: dict[int, int] = field(default_factory=dict)  # id -> duracion_min
    pacientes: dict[int, str] = field(default_factory=dict)
    turnos: list[TurnoData] = field(default_factory=list)
    auditoria: list[AuditoriaData] = field(default_factory=list)
    _next_id: int = 1
    _next_auditoria_id: int = 1


def seed_ficticio() -> InMemoryAgendaStore:
    """Seed ficticio (RN11): 2 prof, Box 1/2, 5 prestaciones, 3 pacientes, 4 turnos sin choques."""
    store = InMemoryAgendaStore(
        profesionales={1: "Dra. Ficticia Uno", 2: "Dr. Ficticio Dos"},
        sillones={1: "Box 1", 2: "Box 2"},
        prestaciones={1: 30, 2: 15, 3: 20, 4: 45, 5: 60},
        pacientes={1: "Paciente Ficticio A", 2: "Paciente Ficticio B", 3: "Paciente Ficticio C"},
    )
    seed_turnos = [
        (1, 1, 1, 1, datetime(2026, 10, 15, 9, 0, tzinfo=AR), datetime(2026, 10, 15, 9, 30, tzinfo=AR)),
        (1, 1, 2, 2, datetime(2026, 10, 15, 10, 0, tzinfo=AR), datetime(2026, 10, 15, 10, 15, tzinfo=AR)),
        (2, 2, 4, 3, datetime(2026, 10, 15, 9, 0, tzinfo=AR), datetime(2026, 10, 15, 9, 45, tzinfo=AR)),
        (2, 2, 1, 1, datetime(2026, 10, 15, 11, 0, tzinfo=AR), datetime(2026, 10, 15, 11, 30, tzinfo=AR)),
    ]
    for i, (prof, sil, prest, pac, ini, fin) in enumerate(seed_turnos, start=1):
        store.turnos.append(
            TurnoData(id=i, profesional_id=prof, sillon_id=sil, prestacion_id=prest,
                      paciente_id=pac, inicio=ini, fin=fin, token_publico=f"tok-seed-{i}")
        )
    store._next_id = 5
    return store


class _TurnoRepo:
    def __init__(self, uow: "InMemoryUoW") -> None:
        self._uow = uow

    async def crear(self, *, profesional_id: int, sillon_id: int, prestacion_id: int,
                    paciente_id: int, inicio: datetime, fin: datetime,
                    estado: str = "reservado", token_publico: str = "") -> TurnoData:
        turno = TurnoData(
            id=self._uow._store._next_id, profesional_id=profesional_id, sillon_id=sillon_id,
            prestacion_id=prestacion_id, paciente_id=paciente_id, inicio=inicio, fin=fin,
            estado=estado, token_publico=token_publico,
        )
        self._uow._store._next_id += 1
        self._uow._pend_turnos.append(turno)
        return turno

    async def activos(self) -> list[TurnoData]:
        return [t for t in self._uow._store.turnos if t.estado != "cancelado"]


class _AuditoriaRepo:
    def __init__(self, uow: "InMemoryUoW") -> None:
        self._uow = uow

    async def registrar(self, *, turno_id: int, accion: str, actor: str) -> AuditoriaData:
        entry = AuditoriaData(id=self._uow._store._next_auditoria_id, turno_id=turno_id,
                              accion=accion, actor=actor)
        self._uow._store._next_auditoria_id += 1
        self._uow._pend_auditoria.append(entry)
        return entry


class InMemoryUoW:
    """UnitOfWork en memoria: `commit()` persiste turno+auditoría juntos; si se
    sale del contexto sin commit (o con excepción) se descarta lo staged."""

    def __init__(self, store: InMemoryAgendaStore) -> None:
        self._store = store
        self.turnos = _TurnoRepo(self)
        self.auditoria = _AuditoriaRepo(self)
        self._pend_turnos: list[TurnoData] = []
        self._pend_auditoria: list[AuditoriaData] = []
        self._committed = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None,
                        exc: BaseException | None,
                        tb: TracebackType | None) -> None:
        if exc_type is not None or not self._committed:
            self._pend_turnos.clear()
            self._pend_auditoria.clear()

    async def commit(self) -> None:
        self._store.turnos.extend(self._pend_turnos)
        self._store.auditoria.extend(self._pend_auditoria)
        self._pend_turnos.clear()
        self._pend_auditoria.clear()
        self._committed = True

    async def rollback(self) -> None:
        self._pend_turnos.clear()
        self._pend_auditoria.clear()
        self._committed = False
