"""RED task 2.1: valida() puro — fin por prestación, [inicio,fin), RN1+RN2.

AAA, un comportamiento por test, sin PG.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

AR = ZoneInfo("America/Argentina/Buenos_Aires")


def _nuevo(inicio, duracion_min=30, prof=1, sillon=1):
    from domain.agenda import NuevoTurno

    return NuevoTurno(
        profesional_id=prof, sillon_id=sillon, inicio=inicio, duracion_min=duracion_min
    )


def _existente(inicio, fin, prof=1, sillon=1, id_=7):
    from domain.agenda import TurnoExistente

    return TurnoExistente(
        id=id_, profesional_id=prof, sillon_id=sillon, inicio=inicio, fin=fin
    )


def test_valida_feliz_calcula_fin_por_prestacion():
    from domain.agenda import valida

    inicio = datetime(2026, 10, 15, 10, 0, tzinfo=AR)
    fin = valida(_nuevo(inicio, duracion_min=30), [])
    assert fin == datetime(2026, 10, 15, 10, 30, tzinfo=AR)


def test_valida_choque_profesional_lanza_409_identificado():
    from domain.agenda import SolapamientoError, valida

    existente = _existente(
        datetime(2026, 10, 15, 10, 0, tzinfo=AR),
        datetime(2026, 10, 15, 10, 30, tzinfo=AR),
    )
    nuevo = _nuevo(datetime(2026, 10, 15, 10, 15, tzinfo=AR))
    try:
        valida(nuevo, [existente])
    except SolapamientoError as e:
        assert e.conflicto.codigo == "PROFESIONAL_OCUPADO"
        assert e.conflicto.existente.id == 7
    else:
        raise AssertionError("debió solapar por profesional")


def test_valida_borde_fin_igual_inicio_permitido():
    from domain.agenda import valida

    existente = _existente(
        datetime(2026, 10, 15, 10, 0, tzinfo=AR),
        datetime(2026, 10, 15, 10, 30, tzinfo=AR),
    )
    fin = valida(_nuevo(datetime(2026, 10, 15, 10, 30, tzinfo=AR)), [existente])
    assert fin == datetime(2026, 10, 15, 11, 0, tzinfo=AR)


def test_valida_fecha_naive_se_rechaza():
    from domain.agenda import FechaInvalida, valida

    try:
        valida(_nuevo(datetime(2026, 10, 15, 10, 0)), [])  # noqa: DTZ001 (naive intencional)
    except FechaInvalida:
        pass
    else:
        raise AssertionError("naive debió rechazarse")


def test_valida_choque_sillon_con_profesional_libre():
    from domain.agenda import SolapamientoError, valida

    existente = _existente(
        datetime(2026, 10, 15, 10, 0, tzinfo=AR),
        datetime(2026, 10, 15, 10, 30, tzinfo=AR),
        prof=99,  # otro profesional
    )
    nuevo = _nuevo(datetime(2026, 10, 15, 10, 15, tzinfo=AR), prof=1, sillon=1)
    try:
        valida(nuevo, [existente])
    except SolapamientoError as e:
        assert e.conflicto.codigo == "SILLON_OCUPADO"
        assert e.conflicto.recurso == "sillon"
    else:
        raise AssertionError("debió solapar por sillón")


def test_valida_duracion_variable_cambia_el_intervalo():
    from domain.agenda import SolapamientoError, valida

    existente = _existente(
        datetime(2026, 10, 15, 11, 0, tzinfo=AR),
        datetime(2026, 10, 15, 11, 30, tzinfo=AR),
    )
    inicio = datetime(2026, 10, 15, 10, 45, tzinfo=AR)
    try:
        valida(_nuevo(inicio, duracion_min=20), [existente])  # fin 11:05 → choca
    except SolapamientoError as e:
        assert e.conflicto.codigo == "PROFESIONAL_OCUPADO"
    else:
        raise AssertionError("20 min debió chocar")
    fin = valida(_nuevo(inicio, duracion_min=15), [existente])  # fin 11:00 → borde
    assert fin == datetime(2026, 10, 15, 11, 0, tzinfo=AR)


def test_valida_duracion_no_positiva_es_422():
    from domain.agenda import FechaInvalida, valida

    try:
        valida(_nuevo(datetime(2026, 10, 15, 10, 0, tzinfo=AR), duracion_min=0), [])
    except FechaInvalida:
        pass
    else:
        raise AssertionError("duración 0 debió rechazarse")


def test_detectores_de_borde_horario_con_zona_dst():
    from zoneinfo import ZoneInfo

    from domain.agenda import _es_ambigua, _es_inexistente

    ny = ZoneInfo("America/New_York")
    # 2026-11-01 01:30 existe dos veces (fin DST) → ambigua
    assert _es_ambigua(datetime(2026, 11, 1, 1, 30), ny) is True  # noqa: DTZ001 (wall time intencional)
    # 2026-03-08 02:30 no existe (inicio DST) → inexistente
    inexistente = datetime(2026, 3, 8, 2, 30, tzinfo=ny)
    assert _es_inexistente(inexistente, ny) is True
    # hora normal no es ni ambigua ni inexistente
    normal = datetime(2026, 10, 15, 10, 0, tzinfo=ny)
    assert _es_ambigua(datetime(2026, 10, 15, 10, 0), ny) is False  # noqa: DTZ001 (wall time intencional)
    assert _es_inexistente(normal, ny) is False
