# Design — c-03-crear-turno-anti-solapamiento

## Context

Repo sin backend aún (`README.md` de 1 línea; no hay `backend/`). Ver propuesta (Why) y
`specs/agenda/crear-turno/spec.md` para el contrato. Restricciones duras: routers thin +
services con commit/rollback; SQLAlchemy async; `EXCLUDE USING gist` como árbitro; TZ
`America/Argentina/Buenos_Aires` + `[inicio, fin)`; datos ficticios; tests por `README.md`;
Conventional Commits. C-02 se resuelve con stub (supuesto, no bloqueo).

## Goals / Non-Goals

**Goals:**
- `dominio_agenda.valida()` puro y determinístico (sin I/O) testeable sin PG.
- `POST /api/turnos` thin → service → repo async; `201`/`409`/`422` contractuales.
- Concurrencia real arbitrada por PG `EXCLUDE`; app precheck solo para mensaje 409 amable.
- Scaffolding autocontenido que corre con lo que diga `README.md` (tests unitarios sin infra externa).

**Non-Goals:**
- SPA; RN8 sobreturnos; RN4/RN9 ciclo de vida; RN7 bloqueos; RN5 MP; lista de espera;
  `GET /api/disponibilidad` en cualquier forma (pertenece a C-05/C-06; este change no expone ningún endpoint de disponibilidad).

## Decisions

1. **Dominio puro `backend/src/domain/agenda.py` (`valida(nuevo, existentes) -> fin | Conflicto`)**
   - Rationale: aritmética `[inicio, fin)` testeable sin DB; RN1 y RN2 en paralelo, ambas deben pasar.
   - Alternativa descartada: validar solo en SQL — pierde tests inmediatos sin infra.
2. **Service `crear_turno()` con commit/rollback; `IntegrityError` de exclusión → 409 dominio**
   - Rationale: regla dura 4/5 — router no decide; el precheck puede sufrir race, el EXCLUDE no.
   - Alternativa descartada: lock aplicativo — no escala y complica el stub.
3. **Modelos mínimos: `Profesional, Sillon, Prestacion, Paciente(min), Turno, Auditoria`**
   - `Turno`: `inicio/fin timestamptz`, `estado=reservado`, `origen`, `token_publico` (opaco, base RN12 futura);
     índices `(profesional_id, inicio, fin)`, `(sillon_id, inicio, fin)` + 2 constraints EXCLUDE
     (uno por profesional, uno por sillón) sobre `tstzrange(inicio, fin, '[)')`.
   - `Prestacion.duracion_min > 0 CHECK`; `Paciente`: nombre+dni único+teléfono obligatorio (RN12 mínimo).
4. **Auth stub `auth_stub.py`: `get_current_user()` fake + `require_role` no-op documentado**
   - Rationale: autocontenido sin C-02; el cableado (Bearer/JWT) queda listo para sustituir.
   - Alternativa descartada: sin auth — ocultaría el punto de integración con C-02.
5. **TZ: `zoneinfo("America/Argentina/Buenos_Aires")`; Pydantic rechaza naive y fechas
   ambiguas/inexistentes (fold/gap) con 422; `TZ` env solo operativo, nunca sustituto del parse.**

## Risks / Trade-offs

- [Race precheck vs EXCLUDE] → el mensaje 409 amable viene del precheck, pero la verdad la dice
  el constraint; el service mapea `IntegrityError` a `PROFESIONAL_OCUPADO`/`SILLON_OCUPADO` por
  constraint name. Tests de doble-reserva concurrente solo contra PG real.
- [Stub-auth se queda pegado] → Mitigación: `README` + design marcan el stub como supuesto
  temporal con tarea de reemplazo en C-02; ningún test depende de permisos reales.
- [EXCLUDE exige `btree_gist`] → Migración crea la extensión; si el entorno PG de cátedra no la
  permite, documentar fallback (índice + 409 por precheck) como pregunta abierta, sin cambiar el spec.
- [Disponibilidad fuera de alcance] → `GET /api/disponibilidad` pertenece a C-05/C-06;
  este change es estrictamente atómico (`POST /api/turnos` + `valida()`) y no expone
  ningún endpoint de disponibilidad.

## Migration Plan

- Sin datos que migrar (greenfield). Alembic `0002_agenda` crea extensión + tablas + EXCLUDE +
  seed ficticio (2 profesionales, 2 sillones Box 1/2, 5 prestaciones, 3 pacientes, 4 turnos sin choques).
- Rollback: `alembic downgrade -1` elimina lo creado; auditoría append-only no se purga en prod,
  solo en dev/test.
- Deploy: `docker compose up --build` (api/db) + `pytest` según `README.md`; variables
  `DATABASE_URL`, `JWT_SECRET` (stub acepta dummy), `TZ=America/Argentina/Buenos_Aires`.

## Open Questions

- Ninguna que cambie spec/enfoque/tasks. Solo registrar en archive si el entorno de cátedra
  limita `btree_gist` o exige entrega sin Docker (entonces tests PG pasan a opt-in con marker).
