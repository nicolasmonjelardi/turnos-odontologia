# Proposal — c-03-crear-turno-anti-solapamiento

> Nota de nombre: CHANGES.md lo nombra `C-03-crear-turno-anti-solapamiento` (mayúscula).
> La CLI `openspec` exige kebab-case minúscula, por eso el change vive como
> `c-03-crear-turno-anti-solapamiento`. Mismo change, solo normalización de caso.

## Why

Este es el change recomendado por la cátedra: el núcleo diferenciador de la agenda es impedir
doble-reserva por profesional y por sillón a la vez. Es un ciclo OPSX único y chico
(RN1+RN2+RN3 verificables por test) que desbloquea todo el dominio (C-04 → C-13).

## What Changes

- `dominio_agenda.valida()`: `fin = inicio + prestacion.duracion_min` (RN3); intervalos
  semiabiertos `[inicio, fin)`; choque si `nuevo.inicio < existente.fin AND nuevo.fin > existente.inicio`;
  borde `fin == inicio` permitido; RN1 y RN2 se evalúan en paralelo y ambas deben pasar.
- `POST /api/turnos`: calcula fin, valida, persiste estado `reservado` + entrada de auditoría
  append-only; `201` en creación con `response_model`; `409 PROFESIONAL_OCUPADO` /
  `SILLON_OCUPADO` con conflicto identificado; `422` en fin inválido / fechas ambiguas (RN10).
- Persistencia SQLAlchemy **async** sobre PostgreSQL 15; el árbitro final de concurrencia es
  `EXCLUDE USING gist` en `(profesional|sillon, rango)`; el precheck de app no decide, solo mapea a 409.
- Scaffolding mínimo autocontenido `backend/src` + stub/mock de usuario/rol para auth
  (C-01/C-02 reales van después; documentado como supuesto en design). Sin SPA en este change
  (la cátedra permite API/módulo sin GUI).
- Tests pytest determinísticos e inmediatos siguiendo únicamente `README.md`:
  dominio puro sin PG obligatorio; escenario API con httpx solo donde aporte sin inflar infra.
- Datos ficticios en seeds/tests (RN11, Ley 25.326). TZ fija `America/Argentina/Buenos_Aires`
  en toda operación de agenda; nada naive ni UTC directo en la lógica (regla dura 9).
- Routers thin → services con commit/rollback; `IntegrityError` → error de dominio (regla dura 4).
  Conventional Commits incrementales (regla dura 10); spec es contrato (regla dura 2).

**Fuera de alcance explícito (no se implementa aunque CHANGES.md §C-03 lo mencione en general):**
SPA React/Vite de agenda; `GET /api/disponibilidad` en cualquier forma (pertenece a C-05/C-06);
RN8 sobreturnos (`sobreturno=true` + rol → va a C-04/C-05);
RN4/RN9 reprogramar-cancelar-confirmar (C-04); RN7 bloqueos (C-05); RN5 señas/MP; lista de espera.

**Contexto de explore (contrato cerrado con el usuario, no reabrir):**
scope recortado sin-SPA; change autocontenido con stub-auth; `dominio_agenda.valida()`
determinístico; governance CRÍTICO con escenarios dado/cuando/entonces
(feliz / solapamiento 409 / borde / duración variable).

## Capabilities

### New Capabilities

- `agenda/crear-turno`: crear un turno con anti-solapamiento por profesional (RN1) y por
  sillón (RN2), duración por prestación (RN3), borde semiabierto e huso AR (RN10),
  persistencia `reservado` + auditoría, y errores 409/422 contractuales.

### Modified Capabilities

(none — primer spec de agenda; no hay capabilities existentes que cambiar)

## Impact

- Código nuevo: `backend/src/{domain,routers,services,repos,auth_stub,main}` + `tests/`
  (unitarios dominio + escenarios API mínimos); `docker-compose` mínimo api/db documentado
  como supuesto si PG se usa como árbitro (tests de dominio no lo exigen).
- APIs nuevas: `POST /api/turnos` (único endpoint de este change).
  Sin breaking changes (API nueva).
- Dependencias: C-02 resuelta con stub documentado (CHANGES.md la declara; este change no la espera).
  Desbloquea C-04/C-05/C-08/C-09 (GATE 3).
