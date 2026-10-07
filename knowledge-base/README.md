# turnos-odontologia — Base de Conocimiento

Sistema de gestión de turnos y agenda para consultorios odontológicos (mercado argentino). Fuente: `docs/discovery/informe-discovery.md` (final 2026-10-07, 18 sistemas) + `discovery` de `.active-orchestrator-state.json`. Integrante: Monjelardi Nicolás. **Sin datos reales de pacientes (solo ficticios).**

## Índice de Archivos

| Archivo | Contenido |
|---------|-----------|
| [01_vision_y_objetivos.md](01_vision_y_objetivos.md) | Propósito, objetivos por actor, alcance MVP (D3), fuera de alcance, métricas |
| [02_descripcion_general.md](02_descripcion_general.md) | Stack oficial (FastAPI+PostgreSQL+Redis+Docker / React+TS+Vite), arquitectura API-first, integraciones, endpoints |
| [03_actores_y_roles.md](03_actores_y_roles.md) | 4 actores, matriz RBAC, rutas públicas sin login |
| [04_modelo_de_datos.md](04_modelo_de_datos.md) | Dominios, ERD, 14 entidades, constraints RN1–RN3, seed ficticia |
| [05_reglas_de_negocio.md](05_reglas_de_negocio.md) | RN1–RN12 (solapamientos, duración, antelación, señas MP, OS/trazabilidad/firma) |
| [06_funcionalidades.md](06_funcionalidades.md) | US por épica del MVP + post-MVP |
| [07_flujos_principales.md](07_flujos_principales.md) | 6 flujos (crear turno anti-solapamiento, reserva, clínica, caja, lista de espera) |
| [08_arquitectura_propuesta.md](08_arquitectura_propuesta.md) | Patrones, directorios backend FastAPI + frontend React/Vite, seguridad JWT Ley 25.326, env vars |
| [09_decisiones_y_supuestos.md](09_decisiones_y_supuestos.md) | DD-01–DD-06 (stack oficial, API+SPA, puertos AFIP/perio, Redis async, Docker Compose) + SU-01–SU-04 |
| [10_preguntas_abiertas.md](10_preguntas_abiertas.md) | AJ-01/AJ-02, "No evidenciado" (AFIP, periodontograma, auditoría, API), verificación V1–V6 |

## Quick Start para Desarrolladores

1. Entender el dominio → [01](01_vision_y_objetivos.md), [03](03_actores_y_roles.md)
2. Entender los datos → [04](04_modelo_de_datos.md)
3. Entender las reglas → [05](05_reglas_de_negocio.md)
4. Entender la arquitectura → [02](02_descripcion_general.md), [08](08_arquitectura_propuesta.md)
5. Implementar → [07](07_flujos_principales.md), [06](06_funcionalidades.md) — empezar por `POST /turnos` anti-solapamiento
6. Antes de codificar → [10](10_preguntas_abiertas.md)

## Resumen Ejecutivo

El mercado AR no combina agenda sin solapamientos + odontograma + Mercado Pago + OS/liquidaciones en un solo producto con precio ARS. El MVP v1 es una API testeable por escenario cuyo diferenciador es anti-solapamiento por profesional Y sillón con duración variable, reserva 24/7 sin login, señas MP y liquidaciones; AFIP/ARCA, periodontograma, auditoría formal y API pública quedan como roadmap explícito.
