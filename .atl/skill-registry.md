# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

Project: turnos-odontologia (odontología AR — Backend Python+FastAPI+JWT+SQLAlchemy+PostgreSQL+Redis+Docker / Frontend React+TS+Vite, tests pytest+httpx). Knowledge: `knowledge-base/` (RN1-RN12, MVP). Roadmap: `CHANGES.md` (17 changes).

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| Building or reviewing FastAPI apps — Pydantic schemas, dependencies, async handlers, auth, or tests | fastapi-patterns | .agents/skills/fastapi-patterns/SKILL.md |
| React components, pages, data fetching, bundle optimization, or performance improvements | vercel-react-best-practices | .agents/skills/vercel-react-best-practices/SKILL.md |
| Writing Python tests, setting up test suites, or implementing testing best practices | python-testing-patterns | .agents/skills/python-testing-patterns/SKILL.md |
| Creating/altering Postgres tables, columns, schemas, migrations, RLS, indexes, triggers, functions; diagnosing slow queries, locking, connection issues | supabase-postgres-best-practices | .agents/skills/supabase-postgres-best-practices/SKILL.md |
| Creating or reviewing Dockerfiles and Compose services, container security/networking/volumes | docker-patterns | .agents/skills/docker-patterns/SKILL.md |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### fastapi-patterns
- Layout: `app/` (main, config, dependencies, database, routers, models, schemas, services) + `tests/` (conftest, test_*.py).
- App factory `create_app()` + async `lifespan`; CORS from settings; `include_router` per domain with prefix/tags.
- Config via pydantic-settings `BaseSettings` (.env file); v2 list literals are safe.
- Schemas Pydantic v2: Base/Create/Update/Response split; `from_attributes=True` on responses; `Field` constraints; `model_validator` for cross-field checks.
- DI via `Annotated` aliases (`DbDep`, `CurrentUserDep`, `ActiveUserDep`); `get_db` rolls back on exception.
- JWT: `OAuth2PasswordBearer`, decode `sub`→int defensively; 401 invalid credentials vs 403 inactive — keep auth and authz checks separate.
- Routers thin: always declare `response_model` (prevents PII leaks); 201 on create; map domain errors to HTTP in router; paginate with skip/limit + `order_by(id)`.
- Services own transactions: commit/rollback, `IntegrityError`→domain error (requires real DB unique constraint); no business logic in route handlers.
- Async SQLAlchemy only (`await db.execute(select(...))`); never sync `Session.query` inside async routes (blocks event loop).
- Tests: httpx `ASGITransport` + `dependency_overrides[get_db]`; autouse create/drop tables; `registered_user` / `auth_token` / `auth_client` fixtures.

### vercel-react-best-practices
- NOTE: frontend is a Vite SPA (no Next.js/SSR) — ignore all RSC/SSR/server-action rules; only client/bundle/render rules apply.
- Parallelize independent fetches with `Promise.all()`; start promises early, await late; `Suspense` boundaries so agenda shell paints while slots stream in.
- Import directly, avoid barrel files; `import()` heavy components (odontograma) on demand; preload on hover/intent; defer analytics/logging until after hydration.
- Prefer statically analyzable import paths (explicit maps of `() => import(...)`, literal paths) to keep bundles narrow.
- Derive state during render, never setState-in-effect for prop changes; functional `setState(curr => ...)`; split independent hooks/effects by dependency.
- Never define components inside components (remounts, focus loss, effect re-runs); pass props; memoize expensive subtrees; lazy `useState(() => ...)` init.
- Deduplicate shared fetches (SWR-style); passive listeners for scroll/touch; version localStorage keys, store minimal fields, always try/catch (incognito/quota throws).
- Explicit ternary (`? : null`), not `&&`, when condition can be `0`/`NaN`; `content-visibility: auto` for long agenda lists; `toSorted()` over `sort()` (no prop mutation).
- JS hot paths: `Map`/`Set` for repeated lookups, combine filter/map passes, early returns, hoist RegExp, `useRef` for transient high-frequency values.

### python-testing-patterns
- AAA structure (Arrange/Act/Assert); name tests `test_<unit>_<scenario>_<expected>`; one behavior per test.
- Layout: `tests/` with `conftest.py` fixtures, split `test_unit/` / `test_integration/` / `test_e2e/`.
- `pytest` fixtures + `parametrize` over duplicated bodies; markers (`slow`, `integration`), `skip`/`skipif`/`xfail` always with reason.
- Mock external deps (`unittest.mock`, `side_effect` lists for retry: fail/fail/ok); unit tests never hit real DB/network.
- `freezegun` `freeze_time` for JWT expiry/scheduling logic; `move_to` for time travel across turno boundaries.
- Async tests need `pytest-asyncio`; autouse setup create/drop tables per test; rollback session after yield.
- Coverage via `pytest-cov --cov-report=term-missing` + fail-under threshold; meaningful coverage over raw %.
- OPSX cycle: every change ships unit + integration tests (httpx client fixtures) proving RN behavior, especially anti-solapamiento.

### supabase-postgres-best-practices
- Load BEFORE any table/column/migration/index/RLS/trigger/function change — even one-column changes or single queries.
- Anti-solapamiento is a DB constraint, not app logic: `EXCLUDE USING gist` on `tstzrange` (requires `btree_gist`), e.g. `(profesional WITH =, sillon WITH =, durante WITH &&)`; app prechecks race — the constraint is the arbiter, map violation to 409 in service.
- Correct types: `timestamptz` for turnos (never naive timestamp); `NOT NULL` + `CHECK` + `UNIQUE`/`FK` in DDL.
- Index every FK and WHERE/ORDER BY column; partial indexes for active/soft-delete filters; verify with `EXPLAIN (ANALYZE, BUFFERS)`, fix seq scans and N+1 first.
- Booking writes: `SELECT ... FOR UPDATE` or advisory locks; keep transactions short; never hold locks across network calls.
- Migrations: additive → backfill → enforce; never rewrite history without a `pg_restore`-tested backup.
- RLS deny-by-default per role (recepcionista/odontólogo/admin); verify policies with role-switched assertions.
- Connections via pooler (transaction mode); set `statement_timeout`; watch for exhaustion, bloat, lock waits in diagnostics.

### docker-patterns
- Compose stack: `api` (dev target, bind mount + `depends_on: db healthy`), `db` (postgres:16-alpine + named volume + init scripts + `pg_isready` healthcheck), `redis` (redis:7-alpine).
- Multi-stage Dockerfile (deps/dev/build/production); bind-mount source for hot reload; anonymous volumes protect container deps/build cache.
- Pin every image tag (never `:latest`).
- Run as non-root `USER`; `no-new-privileges`, `cap_drop: [ALL]`, read-only fs + `tmpfs` where possible.
- Secrets via `env_file`/`.env` (gitignored) or Docker secrets — never hardcoded `ENV` in image or compose.
- Dev vs prod: override file for debug ports; explicit `-f` prod file with `restart` + resource limits; `up --build` to rebuild.
- Services resolve by service name (`db`, `redis`); bind host ports as `127.0.0.1:port` in dev, omit ports in prod.
- `.dockerignore` (`node_modules`, `.git`, `.env`, `dist`, `coverage`); one process per container.
- Platform boundary: Linux containers do NOT validate macOS/Windows behavior — keep a native CI matrix for host paths.

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| (none yet) | — | CLAUDE.md/AGENTS.md do not exist yet — agent-instruction generates them after this pass; conventions section intentionally empty, not an error. |

## Install Decisions

1. fastapi-patterns (INSTALADA): Esencial para arquitectura limpia, inyección de dependencias y rutas del backend base.
2. vercel-react-best-practices (INSTALADA): Proporciona lineamientos y buenas prácticas de tipado para la interfaz de agenda y odontograma.
3. python-testing-patterns (INSTALADA): Imprescindible para estructurar los tests unitarios y de integración con pytest requeridos en el ciclo OPSX.
4. supabase-postgres-best-practices (INSTALADA): Aporta buenas prácticas para constraints e índices de exclusión temporal en PostgreSQL, claves para el anti-solapamiento.
5. sqlalchemy-postgres (DESCARTADA): Redundante, la persistencia básica y modelos quedan cubiertos por fastapi-patterns (#1).
6. docker-patterns (INSTALADA): Asegura un docker-compose reproducible y aislado para PostgreSQL, Redis y la API.
7. vitest (DESCARTADA): Innecesario por el momento; la verificación obligatoria de la cátedra se centra en la lógica de dominio con pytest.
8. mp-integrate (DESCARTADA): Se posterga para la Fase 4 (C-11 caja/señas); en esta etapa priorizamos el núcleo de agenda.
9. integrate-whatsapp (DESCARTADA): Se posterga para C-08; el envío de WhatsApp no forma parte del change nuclear inicial.
10. docker-compose-patterns (DESCARTADA): Redundante con docker-patterns (#6), que ya cubre la orquestación de contenedores.
