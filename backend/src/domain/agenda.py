"""Dominio puro de agenda — change c-03 (RN1+RN2+RN3+RN10).

Sin I/O, sin PG: `valida()` decide con intervalos semiabiertos `[inicio, fin)`.
El árbitro final de concurrencia es el EXCLUDE de Postgres; el precheck de app
solo produce el 409 amable. Huso fijo America/Argentina/Buenos_Aires.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

TZ_AGENDA = ZoneInfo("America/Argentina/Buenos_Aires")


@dataclass(frozen=True)
class NuevoTurno:
    profesional_id: int
    sillon_id: int
    inicio: datetime
    duracion_min: int


@dataclass(frozen=True)
class TurnoExistente:
    id: int
    profesional_id: int
    sillon_id: int
    inicio: datetime
    fin: datetime


@dataclass(frozen=True)
class Conflicto:
    recurso: str  # "profesional" | "sillon"
    codigo: str  # "PROFESIONAL_OCUPADO" | "SILLON_OCUPADO"
    existente: TurnoExistente


class FechaInvalida(ValueError):
    """inicio naive, ambiguo/inexistente en la zona, o fin <= inicio."""


class SolapamientoError(ValueError):
    def __init__(self, conflicto: Conflicto) -> None:
        super().__init__(conflicto.codigo)
        self.conflicto = conflicto


def _es_ambigua(wall_naive: datetime, tz: ZoneInfo) -> bool:
    """True si la hora local mapea a dos instantes UTC (fin de DST)."""
    c0 = wall_naive.replace(tzinfo=tz, fold=0)
    c1 = wall_naive.replace(tzinfo=tz, fold=1)
    return c0.utcoffset() != c1.utcoffset()


def _es_inexistente(inicio: datetime, tz: ZoneInfo) -> bool:
    """True si la hora local no existe (salto de DST): el round-trip la mueve."""
    de_vuelta = inicio.astimezone(timezone.utc).astimezone(tz)
    return de_vuelta.replace(tzinfo=None) != inicio.replace(tzinfo=None)


def _se_solapan(inicio_a: datetime, fin_a: datetime, inicio_b: datetime, fin_b: datetime) -> bool:
    return inicio_a < fin_b and fin_a > inicio_b


def valida(nuevo: NuevoTurno, existentes: Sequence[TurnoExistente]) -> datetime:
    """Valida un turno nuevo y devuelve `fin = inicio + duracion_min` (RN3).

    Lanza `FechaInvalida` (→ 422) o `SolapamientoError` con el conflicto
    identificado (→ 409). RN1 y RN2 se evalúan en paralelo y ambas deben pasar;
    si ambas fallan se reporta profesional primero (orden determinístico).
    """
    if nuevo.duracion_min <= 0:
        raise FechaInvalida("duracion_min debe ser > 0")
    inicio = nuevo.inicio
    if inicio.tzinfo is None:
        raise FechaInvalida("inicio naive: se exige fecha con zona horaria")
    wall = inicio.replace(tzinfo=None)
    if _es_ambigua(wall, TZ_AGENDA):
        raise FechaInvalida("inicio ambiguo en America/Argentina/Buenos_Aires")
    if _es_inexistente(inicio, TZ_AGENDA):
        raise FechaInvalida("inicio inexistente en America/Argentina/Buenos_Aires")
    fin = inicio + timedelta(minutes=nuevo.duracion_min)
    if fin <= inicio:
        raise FechaInvalida("fin <= inicio")

    conflicto_prof: Conflicto | None = None
    conflicto_sillon: Conflicto | None = None
    for ex in existentes:
        if not _se_solapan(inicio, fin, ex.inicio, ex.fin):
            continue
        if ex.profesional_id == nuevo.profesional_id and conflicto_prof is None:
            conflicto_prof = Conflicto("profesional", "PROFESIONAL_OCUPADO", ex)
        if ex.sillon_id == nuevo.sillon_id and conflicto_sillon is None:
            conflicto_sillon = Conflicto("sillon", "SILLON_OCUPADO", ex)
    if conflicto_prof is not None:
        raise SolapamientoError(conflicto_prof)
    if conflicto_sillon is not None:
        raise SolapamientoError(conflicto_sillon)
    return fin
