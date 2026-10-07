# Arquitectura Propuesta

> Stack oficial decidido por el equipo el 2026-10-07 (idem 02; decisión DD-01 en 09): Python + FastAPI + SQLAlchemy/Alembic + PostgreSQL + Redis + Docker Compose / React + TypeScript + Vite. API + worker async + SPA, tests backend con pytest+httpx.

## Patrones aplicados

| Patrón | Dónde se usa | Por qué |
|--------|--------------|---------|
| API-first / capas (routers → servicios/dominio → repositorios) | Toda la API FastAPI | El valor está en la lógica de agenda; testeable sin UI |
| Repositorio sobre ORM | Persistencia PostgreSQL (SQLAlchemy) | Dominio desacoplado del motor; migraciones con Alembic |
| Cola de trabajos async | Redis + worker (recordatorios, confirmaciones, notificaciones) | La reserva responde rápido; el envío/reintento corre en segundo plano |
| Puertos/adaptadores (hexagonal liviano) | MP / WA / GCal / AFIP-futuro | Mocks en tests; AFIP nace como puerto vacío extensible |
| Intervalo semiabierto `[inicio, fin)` | `dominio_agenda` | RN1+RN2 con borde permitido bien definido |
| Auditoría append-only | Cross-cutting | RN6b + base de futura auditoría formal (ver 10) |
| Token público por reserva | Canal paciente | Reserva sin login (RN12) sin exponer IDs internos |

## Estructura de directorios

```
turnos-odontologia/
├── backend/
│   ├── app/
│   │   ├── domain/            # agenda.py (RN1–RN4,RN7–RN9), pagos.py (RN5), cobertura.py (RN6)
│   │   ├── routers/           # turnos, disponibilidad, lista-espera, clinica, caja, admin
│   │   ├── repos/             # repositorios SQLAlchemy (misma interfaz de dominio)
│   │   ├── integrations/      # mercadopago.py, whatsapp.py, gcal.py, afip_stub.py
│   │   ├── auth/              # JWT + RBAC (03), tokens públicos por reserva
│   │   ├── worker/            # jobs Redis: recordatorios, confirmaciones, notificaciones
│   │   └── main.py
│   ├── alembic/               # migraciones (Alembic sobre PostgreSQL)
│   └── tests/
│       └── escenarios/        # solapamiento-profesional, solapamiento-sillon, borde-fin-igual-inicio,
│                              # duracion-variable, antelacion, sena-mp, os-liquidacion, lista-espera (pytest+httpx)
├── frontend/
│   ├── src/                   # SPA React + TypeScript (Vite): agenda, reserva pública, clínica, caja
│   └── package.json           # tests frontend con Vitest + Testing Library (si aplica)
├── docker-compose.yml         # servicios: api, worker, postgres, redis, frontend
├── knowledge-base/
└── docs/discovery/
```

## Seguridad

- Autenticación: JWT (Bearer, expiración corta + refresh) para roles internos; tokens opacos por reserva para canal público.
- Autorización: RBAC según 03 (dependencias por JWT); sobreturnos y anular fuera de plazo solo recepción/admin.
- Validación de input: schemas Pydantic en borde FastAPI; rechazo de fechas ambiguas (RN10).
- Datos de salud: Ley 25.326 — minimización, trazabilidad, exportación; **cero datos reales** en repo/seeds/tests (RN11, solo ficticios).
- Secrets management: solo `.env` local no commiteado; MP/Google creds fuera del repo. `JWT_SECRET` con entropía suficiente y rotación documentada.

## Variables de entorno

| Variable | Descripción | Ejemplo | Sensible |
|----------|-------------|---------|----------|
| `DATABASE_URL` | URL PostgreSQL (SQLAlchemy/Alembic) | `postgresql+psycopg://usuario:clave@postgres:5432/turnos` | Y (lleva credenciales) |
| `REDIS_URL` | URL Redis (cola de trabajos async) | `redis://redis:6379/0` | N |
| `TZ` | Huso horario operativo | `America/Argentina/Buenos_Aires` | N |
| `ANTELACION_MIN_HS` | RN4 (default 24) | `24` | N |
| `MP_ACCESS_TOKEN` | Mercado Pago | `APP_…` | Y |
| `WA_API_TOKEN` | WhatsApp Business | `…` | Y |
| `GCAL_CLIENT_ID/SECRET` | Google Calendar | `…` | Y |
| `JWT_SECRET` | Firma de JWT internos | `…` (generar aleatorio, p. ej. `openssl rand -hex 32`) | Y |
