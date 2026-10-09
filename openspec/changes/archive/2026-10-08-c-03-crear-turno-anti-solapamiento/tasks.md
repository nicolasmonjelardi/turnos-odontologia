# Tasks — c-03-crear-turno-anti-solapamiento

## 1. Scaffolding autocontenido + README como única guía

- [x] 1.1 Crear `backend/src/{domain,routers,services,repos,auth_stub}/` + `main.py` (app factory + lifespan + `GET /api/health`) y verificar `python -m compileall backend/src` en verde
- [x] 1.2 Crear `auth_stub.py` (`get_current_user` fake + `require_role` no-op con `TODO(C-02)`) y verificar import sin JWT real en test de humo
- [x] 1.3 Escribir/actualizar `README.md` (cómo correr `pytest` y `compose up` con `DATABASE_URL/TZ`, supuesto stub-C02, datos ficticios) y verificar que un tercero corre los tests siguiendo solo el README

## 2. Dominio puro determinístico (RN1+RN2+RN3+RN10)

- [x] 2.1 Implementar `domain/agenda.py::valida(nuevo, existentes)` (fin por prestación, `[inicio,fin)`, RN1+RN2 en paralelo, borde permitido, rechazo naive/ambiguo) y verificar con tests AAA `test_*` en verde sin PG
- [x] 2.2 Cubrir escenarios spec: feliz / 409 profesional / 409 sillón / borde `fin==inicio` / duración variable / 422 fecha ambigua, y verificar `pytest backend/tests/test_dominio_agenda.py -q` todo verde

## 3. Modelos + migración PG (árbitro EXCLUDE)

- [x] 3.1 Modelos async `Profesional/Sillon/Prestacion/Paciente(min)/Turno/Auditoria` (`timestamptz`, `duracion_min>0`, índices `(prof|sillon,inicio,fin)`) y verificar `alembic upgrade head` en PG15 local crea tablas
- [x] 3.2 Migración `0002_agenda`: `btree_gist` + 2 `EXCLUDE USING gist` (`profesional` y `sillon` sobre `tstzrange(inicio,fin,'[)')` donde no-cancelado) + seed ficticio (2 prof, Box 1/2, 5 prestaciones, 3 pacientes, 4 turnos sin choques) y verificar seed sin choques + doble-reserva concurrente → `IntegrityError`
- [x] 3.3 Repos async + UnitOfWork (`commit/rollback`) y verificar test de repo crea turno + entrada auditoría en una transacción

## 4. API mínima contractual

- [x] 4.1 `POST /api/turnos` thin (`response_model`, `201`): schema Pydantic TZ-estricta, service calcula fin → precheck `valida()` → persiste `reservado` + auditoría; mapea precheck y `IntegrityError` a `409 PROFESIONAL_OCUPADO`/`SILLON_OCUPADO`, fechas malas a `422`; y verificar `pytest backend/tests/test_api_turnos.py -q` (httpx ASGITransport + overrides) en verde
- [x] 4.2 Documentar en `README.md` el supuesto stub-auth y el recorte (sin SPA, sin RN8, disponibilidad en C-05/C-06) y verificar que `openspec validate c-03-crear-turno-anti-solapamiento` no reporta recorte indebido

## 5. Integración y cierre verificable

- [x] 5.1 Correr suite completa `pytest -q` + `ruff`/`mypy` si el README los declara y verificar todo verde antes de archivar (regla dura 8: nada en rojo)
- [x] 5.2 Checkpoint CRÍTICO: demostrar escenarios gobernanza (feliz 201+auditoría / 409×2 con conflicto / borde permitido / duración variable) y verificar aceptación explícita del usuario antes de `/opsx:archive` — ACEPTADO por el usuario el 2026-10-08 (suite 24 passed + 1 skipped verificada por el orquestador)
