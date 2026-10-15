# Constancia C-01 / C-02 — scaffolding mínimo dentro de C-03

> C-01 y C-02 **no están cerrados**. Este documento deja constancia de qué parte
> se construyó como mínimo autocontenido dentro de C-03 y qué queda pendiente.
> Fecha: 2026-10-14. Autor: Nicolás Monjelardi (entrega individual).

## Por qué se hizo C-03 antes que C-01 y C-02

1. La cátedra exige en la Etapa 6 un **único change chico del MVP con reglas
   verificables**. `CHANGES.md` declara a C-03 `crear-turno-anti-solapamiento`
   (RN1+RN2+RN3) como change recomendado: ciclo OPSX único implementable con
   tests por escenario. Era el único que permitía cerrar explore → propose →
   apply → verify → archive a tiempo (alcance realista: un change bien cerrado
   antes que varios a medias).
2. El orden `C-01 → C-02 → C-03` es **técnico-obligatorio, no académico**.
   Se invirtió a propósito con supuesto explícito en
   `openspec/changes/archive/2026-10-08-c-03-crear-turno-anti-solapamiento/design.md`:
   "C-02 se resuelve con stub (supuesto, no bloqueo)". La cátedra permite
   API o módulo sin GUI, y el contrato de explore cerró scope sin-SPA.
3. No se pretende hacer pasar C-01/C-02 por hechos: se construyó solo el
   mínimo para que C-03 corriera y quedara verificado por `README.md`.

## Qué cubre C-03 (evidencia) y qué queda pendiente

| Ítem C-01 / C-02 | Cubierto en C-03 | Pendiente |
|---|---|---|
| FastAPI mínima + `GET /health` | Sí parcial: `backend/src/main.py` (health + turnos) | Renombrar a `/api/health`, settings `.env`, logger, manejo global |
| `docker-compose.yml` api/db/redis | Sí: servicios api/db/redis, `TZ=America/Argentina/Buenos_Aires` | `worker`, `frontend`, postgres:15 (hay :16), sin defaults hardcodeados |
| Alembic + PostgreSQL único motor | Parcial: `backend/alembic/versions/0002_agenda.py` + `EXCLUDE USING gist` | Migración `0001` (usuarios/roles), CI backend+frontend |
| `frontend/` Vite React 18 TS | No (recorte sin-SPA aprobado en `proposal.md`) | Scaffolding completo (DD-02) |
| Auth JWT + RBAC (C-02) | Solo stub: `backend/src/auth_stub.py` (`get_current_user` fake, `require_role` no-op, `TODO(C-02)`), `JWT_SECRET=dummy` | login/refresh/logout/me, rotación + blacklist, rate limiting, matriz RBAC, tokens opacos reales |
| Tests reproducibles | Sí: `pytest -q` verde sin infra (dominio + API en memoria), PG opt-in | Suite C-01/C-02 (RBAC por rol, CI) |

Ningún test de C-03 depende de permisos reales. La deuda (JWT real,
frontend, migración 0001, RBAC, CI, postgres:15) queda para retomar C-01/C-02.
