"""Router thin POST /api/turnos — change c-03.

`response_model` + `201`. Mapea dominio→HTTP: precheck/`IntegrityError`
→ 409 con conflicto identificado; fechas malas → 422. Sin lógica de negocio.
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import AwareDatetime, BaseModel

from deps import get_store
from domain.agenda import FechaInvalida, SolapamientoError
from repos import InMemoryAgendaStore
from services.turnos import ExclusionRaceError, crear_turno

router = APIRouter(prefix="/api")


class TurnoCreate(BaseModel):
    profesional_id: int
    sillon_id: int
    prestacion_id: int
    paciente_id: int
    inicio: AwareDatetime


class TurnoRead(BaseModel):
    id: int
    profesional_id: int
    sillon_id: int
    prestacion_id: int
    paciente_id: int
    inicio: datetime
    fin: datetime
    estado: str
    token_publico: str


def _error_409_conflicto(codigo: str, existente: Any) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "codigo": codigo,
            "mensaje": f"recurso ocupado: {codigo.lower()}",
            "conflicto": {
                "turno_id": existente.id,
                "inicio": existente.inicio.isoformat(),
                "fin": existente.fin.isoformat(),
            },
        },
    )


@router.post("/turnos", response_model=TurnoRead, status_code=201,
             responses={409: {"description": "solapamiento"}, 422: {"description": "fecha inválida"}})
async def post_turno(payload: TurnoCreate,
                     store: InMemoryAgendaStore = Depends(get_store)) -> TurnoRead | JSONResponse:  # noqa: B008 (idioma FastAPI)
    try:
        turno = await crear_turno(
            store=store, profesional_id=payload.profesional_id, sillon_id=payload.sillon_id,
            prestacion_id=payload.prestacion_id, paciente_id=payload.paciente_id,
            inicio=payload.inicio,
        )
    except SolapamientoError as e:
        return _error_409_conflicto(e.conflicto.codigo, e.conflicto.existente)
    except ExclusionRaceError as e:
        return JSONResponse(status_code=409,
                            content={"codigo": e.codigo, "mensaje": "conflicto de concurrencia"})
    except FechaInvalida as e:
        return JSONResponse(status_code=422,
                            content={"codigo": "FECHA_INVALIDA", "mensaje": str(e)})
    return TurnoRead(id=turno.id, profesional_id=turno.profesional_id, sillon_id=turno.sillon_id,
                     prestacion_id=turno.prestacion_id, paciente_id=turno.paciente_id,
                     inicio=turno.inicio, fin=turno.fin, estado=turno.estado,
                     token_publico=turno.token_publico)
