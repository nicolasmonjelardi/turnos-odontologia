# turnos-odontologia — Instrucciones para Agentes

> Este archivo (y su copia `CLAUDE.md`) es lo PRIMERO que todo agente lee al entrar al repo.
> Generado a partir de `knowledge-base/` y `CHANGES.md`. No editar a mano sin re-sincronizar ambos archivos.

---

## Stack Tecnológico

| Capa | Tecnología oficial | Versión mínima |
|------|--------------------|----------------|
| Lenguaje / runtime backend | Python | Python 3.12 |
| Framework API | FastAPI (Pydantic, OpenAPI automático) | FastAPI 0.110+ |
| ORM / migraciones | SQLAlchemy + Alembic | SQLAlchemy 2.0 |
| Persistencia | PostgreSQL (único motor dev/test/prod) | Postgres 15 |
| Tareas asíncronicas | Redis (recordatorios, confirmaciones, notificaciones) | Redis 7 |
| Autenticación | JWT (roles internos) + token público por reserva | — |
| Contenedores | Docker / Docker Compose | Compose v2 |
| Frontend | React + TypeScript + Vite (SPA) | React 18 / Vite 5 |
| Tests backend | pytest + httpx | pytest 8 |
| Integraciones | Mercado Pago SDK, WhatsApp Business API, Google Calendar API | — |

Detalle completo: [knowledge-base/02_descripcion_general.md](knowledge-base/02_descripcion_general.md)

---

## Base de Conocimiento

La fuente de verdad del dominio vive en `knowledge-base/`. **Leé el archivo relevante ANTES de implementar.**

| Archivo | Cuándo leerlo |
|---------|---------------|
| [01_vision_y_objetivos.md](knowledge-base/01_vision_y_objetivos.md) | Entender propósito y alcance |
| [03_actores_y_roles.md](knowledge-base/03_actores_y_roles.md) | Auth, RBAC, permisos |
| [04_modelo_de_datos.md](knowledge-base/04_modelo_de_datos.md) | Entidades, ERD, migraciones |
| [05_reglas_de_negocio.md](knowledge-base/05_reglas_de_negocio.md) | Reglas codificadas (RN1–RN12) |
| [06_funcionalidades.md](knowledge-base/06_funcionalidades.md) | Historias de usuario por épica |
| [07_flujos_principales.md](knowledge-base/07_flujos_principales.md) | Flujos E2E |
| [08_arquitectura_propuesta.md](knowledge-base/08_arquitectura_propuesta.md) | Patrones, estructura, env vars |
| [10_preguntas_abiertas.md](knowledge-base/10_preguntas_abiertas.md) | ⚠️ Inconsistencias a resolver ANTES de codear |

> ⚠️ Resolver las preguntas de prioridad **Alta** de `10_preguntas_abiertas.md` antes de arrancar el primer change.

---

## Skills Disponibles

| Agente | Rol | Skills que carga |
|--------|-----|------------------|
| **Backend Core** | FastAPI, dominio agenda, anti-solapamiento | `fastapi-patterns`, `python-testing-patterns`, `supabase-postgres-best-practices` |
| **Datos / Infra** | Postgres, migraciones, Compose | `supabase-postgres-best-practices`, `docker-patterns` |
| **Frontend** | React, agenda, odontograma (Vite SPA) | `vercel-react-best-practices` |

Cargá la skill correspondiente al contexto ANTES de escribir código.

> Los compact rules de cada skill los resuelve el orquestador desde `.atl/skill-registry.md` (generado por `skill-registry`; no versionado — no está en el repo). Esta tabla solo mapea skill→rol.

---

## Roadmap de Changes

El plan de implementación completo está en [CHANGES.md](CHANGES.md). Resumen:

- **Total**: 17 changes en 6 fases (C-01 a C-13 = MVP v1; C-14 a C-17 = post-MVP).
- **Camino crítico**: `C-01 → C-02 → C-03 → C-04 → C-06 → C-11 → C-12` (cierre MVP en liquidaciones).
- **Primer change**: `C-01` (foundation-setup). Primer change de dominio: `C-03` (crear-turno-anti-solapamiento, RN1+RN2+RN3 — change recomendado por la cátedra).

**Antes de cualquier `/opsx:propose`**: leé [CHANGES.md](CHANGES.md), identificá las dependencias del change y los archivos de "Leer antes".

---

## Reglas Duras (específicas del proyecto)

> No hay `~/.claude/CLAUDE.md` global en este entorno: las universales mínimas viven acá abajo junto a las del proyecto. Todas fueron confirmadas con el equipo el 2026-10-07. Son contrato; romperlas es un defecto.

1. `NUNCA` persistir ni commitear datos reales de pacientes → solo ficticios en repo, seeds, tests y capturas (RN11, Ley 25.326).
2. `NUNCA` implementar un change sin especificación aprobada → el spec de `propose` es el contrato; lo no especced se vuelve a `propose`, no se inventa en `apply`.
3. `NUNCA` completar por deducción lo marcado "No evidenciado" → se registra en preguntas abiertas.
4. `NUNCA` lógica de negocio en routers FastAPI → services con commit/rollback; routers thin con `response_model` y 201 en creación.
5. `NUNCA` queries síncronas en rutas async → SQLAlchemy async; el anti-solapamiento lo arbitra la BD (`EXCLUDE USING gist`), la app mapea a 409.
6. `NUNCA` usar `any` en TypeScript → tipado estricto, componentes en PascalCase, `tsconfig` estricto.
7. `NUNCA` hardcodear secretos → env vars (`JWT_SECRET`, `DATABASE_URL`, `REDIS_URL`), `.env` gitignored, imágenes pineadas non-root.
8. `NUNCA` buildear, commitear ni pushear sin pedido explícito → tests en verde antes de archivar un change.
9. `NUNCA` manejar fechas/horas naive ni UTC directo en la lógica de agenda → toda operación, validación y persistencia de turnos fija `America/Argentina/Buenos_Aires` (UTC-3); los turnos son intervalos semiabiertos `[inicio, fin)`, `fin == inicio` es borde válido no solapado (RN10).
10. `NUNCA` un único commit acumulado al final → Conventional Commits (`feat:`, `test:`, `docs:`, `chore:`) incrementales por cada etapa de la fundación y fase del ciclo OPSX.

---

## Flujo de Trabajo

```
1. Leer la KB relevante (knowledge-base/)        → entender el dominio
2. Identificar el change en CHANGES.md           → respetar dependencias
3. /opsx:propose C-NN-nombre                     → proposal + design + specs + tasks
4. Implementar las tasks (cargando skills)       → respetando las reglas duras
5. /opsx:archive C-NN-nombre + marcar [x]        → cerrar el change
```

Aplicar TODAS las reglas duras en cada paso. Ante conflicto entre la KB y este archivo, las reglas duras prevalecen.
