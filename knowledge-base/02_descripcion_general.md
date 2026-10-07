# Descripción General

> Stack oficial decidido por el equipo el 2026-10-07 (ver DD-01 en `09_decisiones_y_supuestos.md`). Detalle en `08_arquitectura_propuesta.md`.

## Stack tecnológico

| Capa | Tecnología oficial | Versión mínima | Notas |
|------|--------------------|----------------|-------|
| Lenguaje / runtime backend | Python | Python 3.12 | Decisión del equipo 2026-10-07 |
| Framework API | FastAPI | FastAPI 0.110+ | API REST + validación con Pydantic + OpenAPI automático |
| ORM / migraciones | SQLAlchemy + Alembic | SQLAlchemy 2.0 | Capa de repositorio sobre PostgreSQL |
| Persistencia | PostgreSQL | Postgres 15 | Único motor en dev/test/prod; datos de prueba solo ficticios |
| Tareas asíncronicas | Redis (cola de trabajos: recordatorios, confirmaciones, notificaciones) | Redis 7 | Worker separado; API encola, worker ejecuta y reintenta |
| Autenticación | JWT (roles internos) + token público por reserva | — | JWT para admin/recepción/odontólogo; token opaco para canal paciente sin login (RN12) |
| Contenedores | Docker / Docker Compose | Compose v2 | Servicios: api, worker, postgres, redis, frontend |
| Frontend | React + TypeScript + Vite | React 18 / Vite 5 | SPA para recepción/admin/odontólogo; reserva pública 24/7 |
| Tests backend | pytest + httpx | pytest 8 | Tests por escenario de agenda exigidos por la cátedra |
| Tests frontend (si aplica) | Vitest + Testing Library | Vitest 1 | Solo para componentes del SPA |
| Integraciones | Mercado Pago SDK, WhatsApp Business API (HTTP), Google Calendar API | — | Mockeadas en tests; AFIP/ARCA solo como puerto extensible (no v1) |

## Arquitectura general

API-first monolítica modular (un deployable API + worker, dominios separados) + SPA React/Vite como cliente:

```
Paciente (link 24/7) ──┐
Recepcionista/Admin ────┼──→ SPA React+TS (Vite) ──→ API REST (FastAPI) → Lógica de dominio (agenda/turnos)
Odontólogo ────────────┘                                      │                              │
                                                              ├──→ PostgreSQL (SQLAlchemy/Alembic)
                                                              └──→ Redis (cola: recordatorios,
                                                                       confirmaciones, notificaciones)
                                                              └──→ Adaptadores externos (MP / WA / GCal — mocks en test)
```

Justificación: el diferenciador (anti-solapamiento profesional+sillón, duración variable, lista de espera) vive en el dominio, no en la UI. Una API testeable por escenario (pytest+httpx) cumple la consigna de la cátedra; el SPA React consume el mismo contrato (`available_slots` estilo NexHealth) y deja abierta la API pública del roadmap. Redis absorbe el trabajo diferido (recordatorios, confirmaciones, notificaciones) sin bloquear la reserva.

## Integraciones externas

| Servicio | Propósito | Tipo | Etapa |
|----------|-----------|------|-------|
| WhatsApp Business API | Confirmaciones, recordatorios, avisos de lista de espera | REST/webhook | v1 manual/planificado → auto |
| Google Calendar | Sincronización bidireccional de agenda | REST/OAuth | v1 (referencia: DentalSoft comprobado) |
| Mercado Pago | Cobro de señas y pagos vinculados a reserva | SDK/REST/webhook | v1 |
| AFIP/ARCA | Facturación electrónica | Web service | Post-MVP (hoy "No evidenciado"; puerto extensible, ver 10) |
| Firma digital certificada / Radiología / Marketing | Consentimientos avanzados, Rx, campañas | SDK/REST | Post-MVP |

## API REST (resumen por recurso)

- `GET /disponibilidad?profesional=&sillon=&prestacion=&desde=&hasta=` — slots reales (contrato estilo `available_slots`, ref. NexHealth).
- `POST /turnos` — crea turno evitando solapamientos por profesional y por sillón (change recomendado por la cátedra); 409 ante choque.
- `PATCH /turnos/:id` (reprogramar), `DELETE /turnos/:id` (cancelar con antelación mínima RN4), `POST /turnos/:id/confirmar`.
- `GET/POST /lista-espera` + `POST /lista-espera/:id/reasignar`.
- `GET/POST /pacientes`, `GET/POST /fichas`, `GET/PUT /odontograma/:pacienteId`.
- `GET/POST /presupuestos`, `GET/POST /pagos` (seña MP), `POST /webhooks/mercadopago`.
- `GET/POST /liquidaciones` (por profesional, por OS), `GET /reportes/ocupacion|facturacion`.
- `GET/POST /profesionales|/sillones|/prestaciones|/bloqueos|/obras-sociales`, `GET /export` completo.
