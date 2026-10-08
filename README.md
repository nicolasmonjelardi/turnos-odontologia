# turnos-odontologia — backend c-03 (crear turno anti-solapamiento)

## Requisitos

- Python 3.12+ · PostgreSQL 15+ (solo árbitro PG opt-in) · Redis 7 (no usado en c-03)
- Huso fijo: `America/Argentina/Buenos_Aires` (regla dura 9). Exportar `TZ=America/Argentina/Buenos_Aires`.
- Todos los datos de pacientes son **FICTICIOS** (RN11, Ley 25.326). Nunca commitear datos reales.

## Cómo correr los tests (única guía necesaria)

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

Suite verde = dominio puro + API en memoria, **sin infra externa**.
`python -m compileall -q src` también debe pasar.

## Postgres opt-in (árbitro EXCLUDE, task 3.2)

Por defecto los tests PG se **saltan**. Para correrlos con un Postgres real
con permiso de crear la extensión `btree_gist`:

```bash
cd backend
set TEST_PG=1
set DATABASE_URL=postgresql+asyncpg://usuario:clave@localhost:5432/turnos
pytest -q -m "not skip"
```

Ver `alembic/versions/0002_agenda.py` (migración) y `seed_ficticio.sql`.

## Compose (api/db/redis)

```bash
docker compose up --build
```

Variables: `DATABASE_URL`, `JWT_SECRET` (el stub acepta cualquier dummy en c-03),
`REDIS_URL`, `TZ=America/Argentina/Buenos_Aires`. Ver `.env.example`.
Sin Docker en el entorno de cátedra: los tests de dominio/API siguen verdes sin infra.

## Supuestos declarados (stub-auth + recorte)

- **Stub-auth**: `backend/src/auth_stub.py` (`get_current_user` fake + `require_role`
  no-op). TODO(C-02): reemplazar por JWT real. Ningún test depende de permisos reales.
- **Recorte c-03** (contrato del spec aprobado): solo `POST /api/turnos` + `valida()`.
  Sin SPA · sin sobreturnos RN8 (va a C-04/C-05) · sin reprogramar/cancelar/confirmar
  RN4/RN9 (C-04) · sin bloqueos RN7 (C-05) · sin señas/MP RN5 · sin lista de espera ·
  sin `GET /api/disponibilidad` en ninguna forma (pertenece a C-05/C-06).

## Calidad

```bash
ruff check src tests
mypy src
```
