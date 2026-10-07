# Funcionalidades

> Organizadas por épica según MVP (Discovery §D3). Cada historia mapea a sus RN. Post-MVP marcado explícitamente.

## Épica 1: Agenda anti-solapamiento (diferenciador)

### US-001 — Crear un turno evitando solapamientos por profesional y por sillón/box
**Como** recepcionista **Quiero** crear un turno con duración según prestación **Para** ocupar la agenda sin choques.
**Criterios de aceptación**:
- [ ] El fin se calcula por prestación (RN3) y se valida RN1+RN2; ante choque retorna 409 con el conflicto identificado.
- [ ] El borde `fin == inicio` siguiente está permitido.
- [ ] El sobreturno exige flag + rol y queda diferenciado.
**Reglas relacionadas**: RN1, RN2, RN3, RN8

### US-002 — Reprogramar sin romper la agenda
**Como** recepcionista **Quiero** mover un turno de slot **Para** responder a pedidos del paciente sin generar choques.
**Criterios de aceptación**:
- [ ] Respeta antelación mínima (RN4); revalida RN1+RN2 atómicamente (RN9).
**Reglas relacionadas**: RN1, RN2, RN4, RN9

### US-003 — Bloqueos y disponibilidad real
**Como** administrador **Quiero** cargar bloqueos (feriados/vacaciones) **Para** no ofrecer huecos falsos.
**Criterios de aceptación**:
- [ ] Los bloqueos ocupan el slot igual que un turno (RN7); `GET /disponibilidad` los excluye.
**Reglas relacionadas**: RN7, RN10

### US-004 — Lista de espera con reasignación
**Como** recepcionista **Quiero** anotar pacientes y reasignar cancelaciones **Para** no perder turnos libres.
**Criterios de aceptación**:
- [ ] Reasignar valida RN1+RN2 antes de confirmar.
**Reglas relacionadas**: RN1, RN2

## Épica 2: Reserva online y paciente

### US-010 — Reserva online 24/7
**Como** paciente **Quiero** ver horarios libres reales y reservar sin llamar **Para** no depender del horario de recepción.
**Criterios de aceptación**:
- [ ] Flujo sin login (nombre+DNI+teléfono, RN12); token para gestionar la reserva.
**Reglas relacionadas**: RN12, RN1, RN2, RN3

### US-011 — Confirmar / cancelar / reprogramar (paciente)
**Como** paciente **Quiero** gestionar mi reserva **Para** avisar cambios a tiempo.
**Criterios de aceptación**:
- [ ] Cancela/reprograma hasta antelación mínima (RN4); dispara aviso a lista de espera.
**Reglas relacionadas**: RN4, RN9

### US-012 — Recordatorios
**Como** recepcionista **Quiero** programar recordatorios email/WhatsApp **Para** reducir ausentismo.
**Criterios de aceptación**:
- [ ] Programación 24h + confirmación; costo WA por mensaje documentado (riesgo Discovery §10).
**Reglas relacionadas**: RN4

## Épica 3: Clínica

### US-020 — Ficha + evolución + odontograma
**Como** odontólogo **Quiero** registrar evolución y odontograma en la visita **Para** no duplicar carga.
**Criterios de aceptación**:
- [ ] Odontograma FDI versionado con historial; 18 estados base.
**Reglas relacionadas**: RN6c

### US-021 — Planes y presupuestos con OS
**Como** odontólogo **Quiero** armar plan/presupuesto con cobertura **Para** informar costo real al paciente.
**Criterios de aceptación**:
- [ ] Aplica OS/plan (RN6a); genera consentimiento requerido.
**Reglas relacionadas**: RN6a, RN6c

## Épica 4: Caja y administración

### US-030 — Caja, señas MP y pagos
**Como** recepcionista **Quiero** cobrar señas por Mercado Pago **Para** asegurar la reserva.
**Criterios de aceptación**:
- [ ] Seña atada a reserva (RN5); webhook acredita y confirma.
**Reglas relacionadas**: RN5, RN6b

### US-031 — Liquidaciones y reportes
**Como** administrador **Quiero** liquidar por profesional y por OS **Para** controlar facturación y ocupación.
**Criterios de aceptación**:
- [ ] Liquidación agrupa turnos/pagos del período; reportes de ocupación y facturación.
**Reglas relacionadas**: RN6a, RN6b

### US-032 — Roles, configuración y exportación
**Como** administrador **Quiero** gestionar catálogos y exportar todo **Para** operar sin lock-in.
**Criterios de aceptación**:
- [ ] ABM profesionales/sillones/prestaciones/bloqueos; exportación completa; auditoría consultable.
**Reglas relacionadas**: RN6b, RN11

## Post-MVP (no implementable en v1)

- US-090 AFIP/ARCA, US-091 periodontograma, US-092 imágenes/Rx, US-093 portal paciente, US-094 IA/chatbot, US-095 multi-sucursal avanzada, US-096 API pública, US-097 firma digital certificada.
