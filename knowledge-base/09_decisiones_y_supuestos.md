# Decisiones y Supuestos

## Decisiones documentadas

### DD-01 — Stack oficial: Python + FastAPI + SQLAlchemy + PostgreSQL + Redis + Docker / React + TypeScript + Vite
**Decisión**: implementar el backend en Python 3.12 + FastAPI (JWT para autenticación, SQLAlchemy como ORM con migraciones Alembic, PostgreSQL como persistencia única en dev/test/prod), Redis para tareas asíncronicas (recordatorios, confirmaciones, notificaciones), Docker/Docker Compose para los servicios, y frontend SPA en React + TypeScript + Vite. Tests backend con pytest + httpx (tests frontend, si aplica, con Vitest + Testing Library).
**Contexto**: stack sin decidir (Discovery §9); decisión del equipo del 2026-10-07. La cátedra exige tests por escenario de agenda.
**Alternativas consideradas**: (a) Node.js + framework liviano + SQLite/Postgres — descartada por decisión del equipo 2026-10-07; (b) Backend sin frontend — descartado (el equipo decidió incluir SPA React); (c) Solo SQLite — descartado para prod multi-usuario.
**Justificación**: decisión del equipo; FastAPI aporta validación Pydantic y OpenAPI automático, SQLAlchemy/Alembic versionan el esquema, Redis desacopla el trabajo diferido sin bloquear la reserva, y Compose reproduce el entorno completo.
**Trade-offs aceptados**: PostgreSQL también en dev/test (requiere Docker); el worker Redis suma un servicio a operar desde el día 1.

### DD-02 — API + SPA React, tests por escenario
**Decisión**: el entregable es la API FastAPI + SPA React/Vite + suite backend `tests/escenarios/` con pytest+httpx (solapamiento profesional, solapamiento sillón, borde, duración variable, antelación, seña, OS/liquidación, lista de espera).
**Contexto**: consigna de la cátedra; el diferenciador es lógica, no UI.
**Justificación**: cada RN tiene test dedicado; el SPA y la futura API pública consumen el mismo contrato (`available_slots` estilo NexHealth).

### DD-03 — Reserva pública sin login + mono-consultorio extensible
**Decisión**: canal paciente con nombre+DNI+teléfono y token por reserva; modelo con `sucursal_id` reservado (default único).
**Contexto**: recomendaciones Discovery §11 (evitar fricción de login; no hacer multi-sucursal día 1).
**Justificación**: maximiza conversión de reserva; el modelo ya prevé la extensión sin reescribir.

### DD-04 — AFIP/ARCA y periodontograma fuera de v1 pero con puertos reservados
**Decisión**: `afip_stub.py` + tablas de auditoría y odontograma versionado desde día 1.
**Contexto**: ambos son "No evidenciado" en locales (ver 10); el mercado no los resuelve juntos (vacío C3-1).
**Justificación**: se compite en agenda+MP+OS sin bloquear el roadmap fiscal/clínico.

### DD-05 — Redis para tareas asíncronicas
**Decisión**: Redis como cola de trabajos para recordatorios, confirmaciones y notificaciones (API encola, worker ejecuta con reintento).
**Contexto**: decisión del equipo del 2026-10-07; los envíos no deben bloquear la reserva ni perderse ante un fallo del proveedor.
**Justificación**: desacopla el camino crítico de reserva del envío; permite reintentos y planificación diferida.
**Trade-offs aceptados**: un servicio más en Compose; los jobs deben ser idempotentes.

### DD-06 — Docker / Docker Compose como entorno estándar
**Decisión**: todos los servicios (api, worker, postgres, redis, frontend) se ejecutan vía Docker Compose; PostgreSQL es el único motor en dev/test/prod.
**Contexto**: decisión del equipo del 2026-10-07; evita divergencias entre entornos.
**Justificación**: entorno reproducible con un comando; paridad total con producción.

## Supuestos inferidos

### SU-01 — La disponibilidad cargada es real
**Supuesto**: profesionales y bloqueos se mantienen actualizados. **Origen**: riesgo Discovery §10. **Riesgo si es falso**: huecos falsos y 409 en reserva. **Cómo validar**: recordatorio operativo + reporte de choques evitados.

### SU-02 — WhatsApp tiene costo por mensaje
**Supuesto**: WA automático no es gratis en AR (riesgo Discovery §10). **Origen**: planes con packs (FLAP) y pricing Meta. **Riesgo**: costo imprevisto. **Cómo validar**: cotizar Meta BSP antes de activar auto.

### SU-03 — OS/AFIP no es "un conector más"
**Supuesto**: requiere reglas locales y homologación. **Origen**: evidencia Discovery (nadie local lo resuelve completo). **Riesgo**: subestimar esfuerzo. **Cómo validar**: spike de homologación en fase 2.

### SU-04 — Paciente prefiere reserva online al WhatsApp informal
**Supuesto**: sin validar con usuarios reales (riesgo Discovery §10). **Riesgo**: baja adopción del link 24/7. **Cómo validar**: piloto con 1 consultorio + métrica % online.
