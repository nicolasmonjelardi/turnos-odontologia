# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto **turnos-odontologia** (agenda odontológica AR: anti-solapamiento profesional+sillón, reserva 24/7, clínica, caja MP/OS, liquidaciones).
> Cada change es atómico: un agente puede implementarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de ejecutar cualquier `/opsx:propose`.**

> Alineación MVP (Discovery §D3 + `knowledge-base/01_vision_y_objetivos.md`): los changes **C-01 a C-13** cubren los imprescindibles + diferenciadores v1; los changes **C-14 a C-17** son explícitamente **post-MVP** (etapas posteriores §D3) y van al final en FASE 5. No se inventó ninguna funcionalidad fuera de la KB + Discovery.

---

## Cómo usar este documento

1. Identificar el change a implementar (verificar que sus dependencias están en `openspec/changes/archive/`).
2. Leer los docs de la knowledge-base indicados en "Leer antes".
3. Ejecutar `/opsx:propose <nombre-del-change>`.
4. Al terminar el change, archivarlo con `/opsx:archive <nombre-del-change>`.
5. Marcar el checkbox `[x]` en este archivo.

---

## Árbol de dependencias

```
C-01 foundation-setup
└── C-02 auth-usuarios-roles
    └── C-03 crear-turno-anti-solapamiento     ← CHANGE CÁTEDRA (RN1+RN2+RN3); desbloquea todo el dominio
        ├── C-04 reprogramar-cancelar-confirmar
        │     ├── C-06 reserva-online-publica
        │     │     └── C-11 caja-senas-mercadopago ──╮
        │     └── C-07 lista-espera-reasignacion      │
        ├── C-05 bloqueos-disponibilidad              │
        ├── C-08 recordatorios                        │
        ├── C-09 ficha-evolucion-odontograma          │
        │     └── C-10 presupuestos-planes-os ────────┼──→ C-12 liquidaciones-reportes ★ (cierre MVP)
        └── C-13 admin-catalogos-auditoria-export ────╯     (+ GCal Bidireccional, puerto AFIP stub)
              └── FASE 5 post-MVP: C-14 afip-arca · C-15 clinica-avanzada · C-16 portal-ia-campanas · C-17 multisucursal-api-firma
```

### Paralelismo por fase

> Cada "gate" es un punto de sincronización. Los changes dentro de un grupo pueden ejecutarse en paralelo.

```
GATE 0: ninguna
  → C-01 foundation-setup (solo)

GATE 1: C-01 ✓
  → C-02 auth-usuarios-roles (solo)

GATE 2: C-02 ✓
  → C-03 crear-turno-anti-solapamiento (solo — change cátedra, base de todo el dominio)

GATE 3: C-03 ✓                     ← PRIMER FORK (4 paralelos)
  → C-04 reprogramar-cancelar-confirmar   [Agente A]
  → C-05 bloqueos-disponibilidad          [Agente B]
  → C-08 recordatorios                    [Agente B — si C-05 ✓]
  → C-09 ficha-evolucion-odontograma      [Agente C]

GATE 4: C-04 ✓
  → C-06 reserva-online-publica           [Agente A]
  → C-07 lista-espera-reasignacion        [Agente B]

GATE 5: C-09 ✓ / C-06 ✓
  → C-10 presupuestos-planes-os           [Agente C — si C-09 ✓]
  → C-11 caja-senas-mercadopago           [Agente A — si C-06 ✓]
  → C-13 admin-catalogos-auditoria-export  [Agente B]

GATE 6: C-10 + C-11 ✓
  → C-12 liquidaciones-reportes           [Agente A]  ★ cierre MVP

GATE 7 (post-MVP): C-12 + C-13 ✓
  → C-14 afip-arca                        [Agente A]
  → C-15 clinica-avanzada                 [Agente B]
  → C-16 portal-ia-campanas               [Agente C]
  → C-17 multisucursal-api-firma          [Agente B — si C-14 ✓]
```

### Camino crítico (7 changes — mínimo irreducible)

```
C-01 → C-02 → C-03 → C-04 → C-06 → C-11 → C-12
```

> El primer change **de dominio** del camino crítico es `C-03 crear-turno-anti-solapamiento`: el change recomendado por la cátedra (RN1+RN2+RN3), implementable como ciclo OPSX único y chico con reglas verificables. Va tercero solo por orden técnico obligatorio (infra C-01 → auth C-02). `C-12` requiere además la rama clínica `C-03 → C-09 → C-10` (prerrequisito paralelo, no parte de la cadena lineal). `C-13` cierra lo transversal (catálogos, auditoría consultable, exportación, GCal).

### Plan óptimo con 3 agentes

```
Paso │ Agente A (Backend Core)      │ Agente B (Backend Aux)         │ Agente C (Frontend/Clínica)
─────┼──────────────────────────────┼────────────────────────────────┼─────────────────────────────
  1  │ C-01 foundation-setup        │               —                │              —
  2  │ C-02 auth-usuarios-roles     │               —                │              —
  3  │ C-03 crear-turno-anti-       │               —                │              —
     │ solapamiento (cátedra)       │                                │
  4  │ C-04 reprogramar-cancelar-   │ C-05 bloqueos-disponibilidad   │ C-09 ficha-evolucion-
     │ confirmar                    │                                │ odontograma
  5  │ C-06 reserva-online-publica  │ C-08 recordatorios             │ C-10 presupuestos-planes-os
  6  │ C-11 caja-senas-mercadopago  │ C-07 lista-espera-             │ C-13 admin-catalogos-
     │                              │ reasignacion                   │ auditoria-export
  7  │ C-12 liquidaciones-reportes ★│               —                │              —
  8* │ C-14 afip-arca               │ C-15 clinica-avanzada          │ C-16 portal-ia-campanas
  9* │               —              │ C-17 multisucursal-api-firma   │              —
```

`* Pasos 8-9 son post-MVP (FASE 5), fuera del MVP v1.`

### Riesgos y supuestos (Discovery §10 + KB 09/10)

- **R1 — WhatsApp tiene costo por mensaje (SU-02)**: WA automático no es gratis en AR (pricing Meta/BSP, planes con packs como FLAP). Mitigación: `C-08` entrega primero email + WA manual/planificado vía worker con reintentos; el envío 100% automático queda como evolución y exige cotizar BSP en ARS antes de activarse.
- **R2 — OS/AFIP no es "un conector más" (SU-03)**: ningún producto local combina OS + AFIP/ARCA en un solo flujo (vacío C3-1). Mitigación: `C-10`/`C-12` resuelven OS + liquidaciones en v1; AFIP/ARCA va como roadmap explícito post-MVP (`C-14`), con `afip_stub.py` como puerto vacío extensible desde `C-13` (DD-04).
- **R3 — Ley 25.326 + datos ficticios (RN11)**: datos personales/salud con trazabilidad; prohibido commitear datos reales en repo, seeds o tests. Mitigación: seeds y tests solo con datos FICTICIOS en todos los changes; auditoría append-only desde `C-03`; exportación completa sin lock-in en `C-13`.
- **R4 — Disponibilidad real (SU-01)**: si profesionales/bloqueos no se mantienen actualizados, se muestran huecos falsos y la reserva devuelve 409. Mitigación: `C-05` (bloqueos como intervalos ocupados) + reporte de choques evitados; `GET /disponibilidad` siempre recalcula contra turnos + bloqueos.
- **R5 — Adopción del canal online (SU-04)**: el paciente podría preferir el WhatsApp informal (no validado con usuarios). Mitigación: reserva sin login (RN12, `C-06`), UX mobile-first tipo Doctolib/Fresha; piloto en 1 consultorio con métrica % online.
- **Preguntas abiertas que condicionan el roadmap (KB 10)**: alcance fiscal de v2 (`C-14`, decidir con contador), nivel de auditoría formal exigible (log consultable v1 en `C-13` vs. pista firmada v2), periodontograma (`C-15`, validar con odontólogo referente).

---

## FASE 0 — Cimientos

### [C-01] `foundation-setup`
- **Estado**: `[ ]` pendiente
- **Scope**: Scaffolding completo + infraestructura base reproducible
  - Estructura de directorios según `08 §Estructura`: `backend/app/{domain,routers,repos,integrations,auth,worker}`, `backend/alembic`, `backend/tests/escenarios`, `frontend/src`
  - `backend/`: FastAPI app mínima con `GET /api/health`, settings por `.env`, logger, manejo de excepciones, `TZ=America/Argentina/Buenos_Aires` (RN10)
  - `docker-compose.yml`: servicios `api, worker, postgres:15, redis:7, frontend`; PostgreSQL único motor en dev/test/prod (DD-06); `DATABASE_URL`, `REDIS_URL` vía `${VAR}` sin defaults hardcodeados
  - `frontend/`: scaffolding Vite + React 18 + TypeScript (DD-02); `.env.example` en cada sub-proyecto con `JWT_SECRET`, `MP_ACCESS_TOKEN`, `WA_API_TOKEN`, `GCAL_CLIENT_ID/SECRET`, `ANTELACION_MIN_HS=24`
  - Alembic inicializado contra PostgreSQL; GitHub Actions CI con jobs paralelos backend (`pytest`) y frontend (build)
- **Dependencias**: ninguna
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios
  - `knowledge-base/08_arquitectura_propuesta.md` §Variables de entorno
  - `knowledge-base/02_descripcion_general.md` §Stack tecnológico
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-01, §DD-05, §DD-06

---

### [C-02] `auth-usuarios-roles`
- **Estado**: `[ ]` pendiente
- **Scope**: Autenticación JWT + RBAC + base de identidad del canal público
  - Modelos: `Usuario` (email único, hash_password, rol admin/recepcionista/odontologo, activo), `Rol`; `sucursal_id` reservado default mono (DD-03)
  - `POST /api/auth/login` — JWT access corto + refresh; rate limiting 5/60s por IP+email; `POST /api/auth/refresh` con rotación y blacklist; `POST /api/auth/logout`; `GET /api/auth/me`
  - Refresh en cookie HttpOnly (secure, samesite=lax); claims JWT `sub, roles, email, jti, type, iat, exp`; `PermissionContext`: `require_role()`, `require_admin()` según matriz RBAC de 03
  - Tokens opacos por reserva para canal público (RN12, base que usa C-06); sobreturnos y anulaciones fuera de plazo solo recepción/admin
  - Migración 001: tablas `usuarios, roles`; seed: 1 admin inicial + roles (datos ficticios, RN11)
  - Tests: login OK, token expirado, refresh rotation, rate limit, matriz RBAC por rol (pytest+httpx)
- **Dependencias**: C-01
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad
  - `knowledge-base/05_reglas_de_negocio.md` §RN12 — Reserva pública mínima

---

## FASE 1 — Agenda anti-solapamiento (diferenciador)

> `C-03` es el change recomendado por la cátedra: ciclo OPSX único y chico, reglas RN1+RN2+RN3 verificables por test.

### [C-03] `crear-turno-anti-solapamiento`
- **Estado**: `[ ]` pendiente
- **Scope**: Crear un turno evitando solapamientos por profesional y por sillón/box (US-001; RN1+RN2+RN3+RN8)
  - Modelos: `Profesional` (matrícula única, horario_semanal JSON), `Sillon` (nombre único por sucursal), `Prestacion` (duracion_min > 0, precio_base, requiere_sillon, color_agenda), `Paciente` mínimo (nombre, dni único, teléfono obligatorio, os_id nullable), `Turno` (inicio/fin tz AR, origen mostrador/online, estado reservado/confirmado/atendido/cancelado/ausente/sobreturno, token_publico), `Auditoria` append-only (quién creó, RN6b)
  - `dominio_agenda.valida()`: `fin = inicio + prestacion.duracion_min` (RN3); intervalos semiabiertos `[inicio, fin)`; choque si `nuevo.inicio < existente.fin AND nuevo.fin > existente.inicio`; borde `fin == inicio` permitido; valida RN1 y RN2 en paralelo, ambas deben pasar
  - `POST /api/turnos` — calcula fin, valida, persiste `reservado` + auditoría; 409 `PROFESIONAL_OCUPADO` / `SILLON_OCUPADO` con conflicto identificado; 422 fin inválido/fechas ambiguas (RN10); sobreturno solo con flag + rol, listado diferenciado (RN8)
  - `GET /api/disponibilidad?profesional=&sillon=&prestacion=&desde=&hasta=` — slots reales estilo `available_slots` (turnos existentes excluidos; bloqueos se integran en C-05)
  - Repositorios SQLAlchemy + UnitOfWork; índices `(profesional_id, inicio, fin)`, `(sillon_id, inicio, fin)`
  - Migración 002: tablas agenda + índices; seed FICTICIO: 2 profesionales, 2 sillones (Box 1/2), 5 prestaciones (consulta 20', limpieza 30', ortodoncia control 30', obturación 45', endodoncia 90'), 3 pacientes, 4 turnos sin choques
  - Tests escenarios (pytest+httpx): `solapamiento-profesional`, `solapamiento-sillon`, `borde-fin-igual-inicio`, `duracion-variable`, doble-reserva concurrente → 409
  - SPA (React/Vite): vista agenda diaria/semanal multi-profesional + multi-sillón que consume `GET /disponibilidad` y `POST /turnos`
- **Dependencias**: C-02
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-001
  - `knowledge-base/05_reglas_de_negocio.md` §RN1–RN3, RN8, RN10
  - `knowledge-base/04_modelo_de_datos.md` §Turno, §Profesional, §Sillon, §Prestacion
  - `knowledge-base/07_flujos_principales.md` §Flujo 1
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones aplicados

---

### [C-04] `reprogramar-cancelar-confirmar`
- **Estado**: `[ ]` pendiente
- **Scope**: Ciclo de vida del turno; antelación mínima; reprogramación atómica (US-002 + US-011 interno; RN4+RN9)
  - `POST /api/turnos/:id/confirmar` — pasa a `confirmado`, encola recordatorio 24h (job Redis que ejecuta C-08)
  - `DELETE /api/turnos/:id` — cancela hasta antelación `ANTELACION_MIN_HS` (default 24h); fuera de plazo → 422 salvo rol recepción/admin + auditoría; libera slot y dispara oferta a lista de espera (hook que consume C-07); con seña aplica política RN5 (hook que usa C-11)
  - `PATCH /api/turnos/:id` (reprogramar) — cancelación + creación atómica bajo RN1+RN2; si el nuevo slot choca → 409 y el original se conserva (RN9); recalcula fin si cambia prestación (RN3)
  - Marca `ausente` para no-shows (insumo de reportes C-12)
  - Sin migración nueva (reutiliza `Turno.estado` + `Auditoria`); config `ANTELACION_MIN_HS` por consultorio
  - Tests: antelación exacta/límite, reprogramación con choque conserva original, cancelación fuera de plazo por rol, confirmación encola recordatorio
- **Dependencias**: C-03
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-002
  - `knowledge-base/05_reglas_de_negocio.md` §RN4, RN9
  - `knowledge-base/07_flujos_principales.md` §Flujo 3
  - `knowledge-base/04_modelo_de_datos.md` §Turno

---

### [C-05] `bloqueos-disponibilidad`
- **Estado**: `[ ]` pendiente
- **Scope**: Bloqueos como intervalos ocupados + disponibilidad real unificada (US-003; RN7+RN10)
  - Modelo `Bloqueo` (profesional_id nullable = general, sillon_id nullable, desde/hasta, motivo feriado/vacaciones/mantenimiento)
  - CRUD `GET/POST/DELETE /api/bloqueos` (solo admin, RBAC 03); `GET /api/disponibilidad` excluye bloqueos igual que turnos (RN7); rechazo de fechas ambiguas/inválidas (RN10)
  - Migración 003: tabla `bloqueos` + índices por rango; seed: 1 bloqueo de feriado ficticio
  - Tests: slot bloqueado no se ofrece, bloqueo general vs. por profesional/sillón, feriado recurrente, TZ `America/Argentina/Buenos_Aires` y transición DST
- **Dependencias**: C-03
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-003
  - `knowledge-base/05_reglas_de_negocio.md` §RN7, RN10
  - `knowledge-base/04_modelo_de_datos.md` §Bloqueo
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-01

---

## FASE 2 — Canal paciente

### [C-06] `reserva-online-publica`
- **Estado**: `[ ]` pendiente
- **Scope**: Reserva online 24/7 sin login + autogestión por token (US-010 + US-011 paciente; RN12+RN4)
  - Rutas públicas (sin JWT, identidad nombre+DNI+teléfono): `GET /api/disponibilidad`, `POST /api/turnos` (origen público → mismo `dominio_agenda.valida()` de C-03, RN1+RN2+RN3), `GET /api/turnos/:token` (ver/cancelar/reprogramar propio hasta antelación RN4), `POST /api/pagos/seña` + `GET /api/presupuestos/:token` (contratos que implementan C-10/C-11)
  - Token opaco por reserva (base C-02); race slot tomado entre consulta y reserva → 409 + slots alternativos (Flujo 2); validación 422 DNI/teléfono; rate limiting público anti-abuso
  - Dispara confirmación WA/email (jobs que ejecuta C-08); si exige seña → link MP (flujo que acredita C-11)
  - Migración 004: extiende `pacientes` (contacto mínimo público) — datos siempre FICTICIOS en tests (RN11)
  - Tests: flujo público E2E sin login, 409 con alternativos, token ajeno → 403, reprogramación/cancelación por token dentro/fuera de antelación
  - SPA: página pública mobile-first de reserva (link compartible, UX tipo Doctolib/Fresha en español rioplatense)
- **Dependencias**: C-04
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-010, §US-011
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas
  - `knowledge-base/05_reglas_de_negocio.md` §RN12, RN4
  - `knowledge-base/07_flujos_principales.md` §Flujo 2
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-03, §SU-04

---

### [C-07] `lista-espera-reasignacion`
- **Estado**: `[ ]` pendiente
- **Scope**: Lista de espera con reasignación validada (US-004; diferenciador v1)
  - Modelo `ListaEspera` (paciente, profesional nullable, prestación, preferencia_horaria, estado pendiente/reasignado/cancelado)
  - `GET/POST /api/lista-espera` + `POST /api/lista-espera/:id/reasignar` — revalida RN1+RN2 antes de confirmar; hook desde cancelación C-04: slot liberado → busca candidatos compatibles → aviso WA/email (jobs C-08); dos candidatos al mismo slot: primero que confirma gana, otro vuelve a espera
  - Migración 005: tabla `lista_espera`; seed: 1 item ficticio
  - Tests escenario `lista-espera`: anotar → cancelar → reasignar OK, reasignación con choque → 409, contención doble candidato
- **Dependencias**: C-04
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-004
  - `knowledge-base/07_flujos_principales.md` §Flujo 6
  - `knowledge-base/04_modelo_de_datos.md` §ListaEspera
  - `knowledge-base/05_reglas_de_negocio.md` §RN1, RN2

---

### [C-08] `recordatorios`
- **Estado**: `[ ]` pendiente
- **Scope**: Recordatorios email + WhatsApp sobre worker Redis (US-012; diferenciador confirmación 24h)
  - Modelo `Recordatorio` (turno, canal email/whatsapp, programado_para, enviado_en, estado)
  - Worker Redis (DD-05): jobs idempotentes `recordatorio_24h`, `confirmacion_reserva`, `aviso_lista_espera` con reintento; API encola, worker ejecuta (la reserva nunca bloquea por el envío)
  - Adaptadores `integrations/whatsapp.py` (Business API) + email con mocks en tests; costo WA por mensaje documentado en README operativo (riesgo R1: primero manual/planificado, auto como evolución tras cotizar BSP en ARS)
  - Confirmación automática 24h (diferenciador v1 si el alcance lo permite)
  - Migración 006: tabla `recordatorios`; Tests: programación 24h, reintento ante fallo proveedor, idempotencia, costo WA documentado
- **Dependencias**: C-03
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-012
  - `knowledge-base/02_descripcion_general.md` §Integraciones externas
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones aplicados (cola async, hexagonal)
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-05, §SU-02
  - `knowledge-base/10_preguntas_abiertas.md` §WhatsApp/BSP

---

## FASE 3 — Clínica

### [C-09] `ficha-evolucion-odontograma`
- **Estado**: `[ ]` pendiente
- **Scope**: Ficha + evolución + odontograma versionado + consentimientos (US-020; RN6c; Ley 25.326)
  - Modelos: `FichaClinica/Evolucion` (paciente, profesional, fecha, anamnesis, evolución, adjuntos_ref), `Odontograma` (pieza FDI 11–48, 18 estados tipo DentalSoft, fecha, version; clave paciente+pieza+version con historial), `Consentimiento` (tipo, texto_version, firma_ref, fecha; RN6c)
  - `GET/POST /api/pacientes`, `GET/POST /api/fichas`, `GET/PUT /api/odontograma/:pacienteId` (RBAC: odontólogo R/W clínica, recepción solo contacto — matriz 03); marcar `atendido` bloqueado si falta consentimiento en plan invasivo (Flujo 4)
  - Minimización de datos de salud + trazabilidad (Ley 25.326); cero datos reales en seeds/tests (RN11, solo ficticios)
  - Migración 007: tablas clínica; seed ficticio: 1 ficha + odontograma ejemplo
  - Tests: versionado odontograma con historial, 18 estados válidos/inválidos, bloqueo `atendido` sin consentimiento, RBAC clínica por rol
  - SPA: vista agenda del día del odontólogo + ficha/evolución + odontograma en la misma visita
- **Dependencias**: C-03
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-020
  - `knowledge-base/04_modelo_de_datos.md` §FichaClinica, §Odontograma, §Consentimiento
  - `knowledge-base/05_reglas_de_negocio.md` §RN6c, RN11
  - `knowledge-base/07_flujos_principales.md` §Flujo 4
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos

---

### [C-10] `presupuestos-planes-os`
- **Estado**: `[ ]` pendiente
- **Scope**: Planes y presupuestos con cobertura OS/prepaga (US-021; RN6a)
  - Modelos: `ObraSocial` (nombre, plan, cobertura_reglas JSON, activa), `Presupuesto/PlanTratamiento` (items prestación+cantidad+precio, os_id/plan + cobertura_aplicada, total, pagado, estado borrador/aprobado/rechazado/en_curso)
  - `GET/POST /api/presupuestos` (+ `GET /api/presupuestos/:token` público, contrato definido en C-06): monto a cargo = total − cobertura; sin OS válida → particular; genera consentimiento requerido (hook C-09)
  - `GET/POST /api/obras-sociales` (ABM admin; catálogo extensible, homologación real queda para v2 — riesgo R2)
  - Migración 008: tablas `obras_sociales, presupuestos`; seed ficticio: "OS Ejemplo Salud" (Básico/Total), "Prepaga Ficticia" (Uno) + 1 presupuesto ejemplo
  - Tests: cobertura aplicada por plan, particular sin OS, estados del plan, consentimiento generado
- **Dependencias**: C-09
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-021
  - `knowledge-base/04_modelo_de_datos.md` §Presupuesto, §ObraSocial
  - `knowledge-base/05_reglas_de_negocio.md` §RN6a
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-03

---

## FASE 4 — Caja y administración

### [C-11] `caja-senas-mercadopago`
- **Estado**: `[ ]` pendiente
- **Scope**: Caja + señas Mercado Pago atadas a la reserva (US-030; RN5+RN6b)
  - Modelo `Pago/Seña` (turno, medio mercadopago/efectivo/transferencia, monto, estado pendiente/aprobado/rechazado/devuelto, mp_payment_id, creado_por)
  - `GET/POST /api/pagos` (+ `POST /api/pagos/seña` público, contrato C-06): reserva con seña queda `reservado` → webhook MP acredita → `confirmado`; seña impaga vencida libera slot + avisa lista de espera (Flujo 1)
  - `POST /api/webhooks/mercadopago` — idempotencia por `mp_payment_id` (webhook duplicado no duplica asientos); anulación/devolución = contra-asiento auditado, nunca borrado físico (RN6b)
  - Adaptador `integrations/mercadopago.py` (puerto hexagonal, mock en tests; credenciales solo `.env`, MP_ACCESS_TOKEN fuera del repo)
  - Migración 009: tablas `pagos, asientos_caja`; Tests escenario `sena-mp`: reserva→seña→webhook→confirmado, webhook duplicado idempotente, vencimiento libera slot, devolución trazada
- **Dependencias**: C-04, C-06
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-030
  - `knowledge-base/05_reglas_de_negocio.md` §RN5, RN6b
  - `knowledge-base/07_flujos_principales.md` §Flujo 1, §Flujo 5
  - `knowledge-base/04_modelo_de_datos.md` §Pago
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad (secrets)

---

### [C-12] `liquidaciones-reportes`
- **Estado**: `[ ]` pendiente
- **Scope**: Liquidaciones por profesional y por OS + reportes (US-031; cierra el MVP)
  - Modelo `Liquidacion` (tipo profesional/os, beneficiario, período, turno_ids, total, estado borrador/cerrada, pdf_ref)
  - `GET/POST /api/liquidaciones` (por profesional y por OS, agrupa turnos/pagos del período; requiere rama C-10 para cobertura OS); `GET /api/reportes/ocupacion|facturacion` (ocupación por profesional/sillón, facturación, ausentismo desde marcas C-04, choques evitados para SU-01)
  - Liquidación cerrada cuadra con caja (métrica éxito 01: conciliación sin reclamos); PDF exportable
  - Migración 010: tabla `liquidaciones`; Tests escenario `os-liquidacion`: agrupa turnos/pagos con cobertura, período exacto, cierre cuadra con caja
- **Dependencias**: C-10, C-11
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-031
  - `knowledge-base/04_modelo_de_datos.md` §Liquidacion
  - `knowledge-base/01_vision_y_objetivos.md` §Métricas de éxito
  - `knowledge-base/07_flujos_principales.md` §Flujo 5

---

### [C-13] `admin-catalogos-auditoria-export`
- **Estado**: `[ ]` pendiente
- **Scope**: ABM de catálogos + GCal + auditoría consultable + exportación + puerto AFIP (US-032; RN6b+RN11)
  - `GET/POST/PUT/DELETE /api/profesionales|/sillones|/prestaciones|/obras-sociales` (solo admin); `GET /api/export` completo sin lock-in; `GET /api/auditoria` consultable (quién creó/movió/canceló/cobró/liquidó — base de futura auditoría formal, ver KB 10)
  - Sincronización bidireccional Google Calendar (`integrations/gcal.py`, OAuth; credenciales en `.env`) — integración imprescindible v1 (Discovery §8)
  - `integrations/afip_stub.py` — puerto vacío extensible para facturación electrónica (DD-04; implementación real en C-14 post-MVP)
  - Gestión de usuarios/roles (solo admin); README operativo + guía de soporte/capacitación inicial (alcance v1)
  - Sin migración nueva (opera sobre tablas existentes); Tests: CRUD catálogos por rol, exportación completa, auditoría registra cada mutación, GCal con mock
- **Dependencias**: C-02, C-03
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-032
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
  - `knowledge-base/02_descripcion_general.md` §Integraciones externas
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-04
  - `knowledge-base/10_preguntas_abiertas.md` §Auditoría formal, §API pública

---

## FASE 5 — Post-MVP (etapas posteriores §D3 — NO implementable en v1)

> Los changes C-14 a C-17 están explícitamente fuera del MVP. Se implementan solo con el MVP (C-01–C-13) cerrado y archivado.

### [C-14] `afip-arca`
- **Estado**: `[ ]` pendiente
- **Scope**: Facturación electrónica AFIP/ARCA sobre el puerto `afip_stub.py` (US-090; "No evidenciado" en locales — KB 10)
  - Implementa `integrations/afip.py` (web service, homologación; alcance fiscal a definir con contador: solo comprobantes vs. liquidación completa)
  - Emite comprobantes desde liquidaciones/pagos C-12/C-11 con trazabilidad RN6b; ambientes homologación/producción separados
  - Migración 011: tablas comprobantes (CAE, estado fiscal); Tests con mock del WS AFIP + homologación documentada
- **Dependencias**: C-12, C-13
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §Post-MVP (US-090)
  - `knowledge-base/01_vision_y_objetivos.md` §Fuera de alcance
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-04, §SU-03
  - `knowledge-base/10_preguntas_abiertas.md` §AFIP/ARCA

---

### [C-15] `clinica-avanzada`
- **Estado**: `[ ]` pendiente
- **Scope**: Periodontograma + imágenes/Rx (US-091, US-092; validar con odontólogo referente — KB 10)
  - Modelo periodontograma (clonar referencia Dentalink/NovusOral solo si el referente lo exige; si basta odontograma, documentar descarte); `adjuntos_ref` de C-09 pasa a storage real de Rx con minimización Ley 25.326
  - `GET/PUT /api/periodontograma/:pacienteId`; `POST /api/imagenes` (referencia radiología externa, etapas posteriores)
  - Migración 012: tablas perio/imágenes; Tests: estados perio, adjunto Rx trazado, RBAC clínica
- **Dependencias**: C-09, C-10
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §Post-MVP (US-091, US-092)
  - `knowledge-base/04_modelo_de_datos.md` §Odontograma, §FichaClinica
  - `knowledge-base/10_preguntas_abiertas.md` §Periodontograma
  - `knowledge-base/05_reglas_de_negocio.md` §RN11

---

### [C-16] `portal-ia-campanas`
- **Estado**: `[ ]` pendiente
- **Scope**: Portal del paciente + IA/chatbot + recuperación y campañas (US-093, US-094; recuperación de ausentes, membresías)
  - Portal paciente con login (evolución del canal sin-login C-06: historial, `check-in QR` opcional); chatbot/IA recepcionista sobre `GET /disponibilidad` + jobs C-08; recuperación de ausentes y campañas (origen: marcas `ausente` C-04)
  - Contratos nuevos versionados sin romper los de C-06; métricas % online (SU-04) como criterio de éxito del piloto
  - Migración 013: credenciales portal, campañas; Tests: login portal, chatbot reserva E2E con mock LLM, campaña recupera ausente
- **Dependencias**: C-06, C-08
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §Post-MVP (US-093, US-094)
  - `knowledge-base/01_vision_y_objetivos.md` §Fuera de alcance
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-04
  - `knowledge-base/03_actores_y_roles.md` §Paciente

---

### [C-17] `multisucursal-api-firma`
- **Estado**: `[ ]` pendiente
- **Scope**: Multi-sucursal avanzada + API pública + firma digital certificada (US-095, US-096, US-097)
  - Activa `sucursal_id` (reservado desde DD-03/C-02): partición de agenda/sillones por sede; congela contrato interno `available_slots` + webhooks (ref. NexHealth) como API pública versionada; consentimientos C-09 migran a firma digital certificada
  - Requiere escala validada (mono-consultorio día 1 — KB 10: validar antes de multi-sucursal)
  - Migración 014: partición por sede, claves API; Tests: aislamiento por sede, contrato público congelado, firma certificada mock
- **Dependencias**: C-13
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §Post-MVP (US-095, US-096, US-097)
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-03
  - `knowledge-base/10_preguntas_abiertas.md` §API pública, §multi-sucursal
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
