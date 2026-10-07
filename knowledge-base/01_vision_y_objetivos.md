# Visión y Objetivos

> Fuente: `docs/discovery/informe-discovery.md` (versión final 2026-10-07) + sección `discovery` de `.active-orchestrator-state.json`. Integrante: Monjelardi Nicolás. Mercado: Argentina. Sin datos reales de pacientes en ningún artefacto (solo ficticios).

## Propósito del sistema

**Brindar a consultorios odontológicos argentinos una agenda confiable que elimina dobles reservas por profesional y por sillón/box, conecta la reserva online 24/7 con la gestión clínica y administrativa, y deja trazabilidad completa de cada turno.**

Los consultorios coordinan hoy por WhatsApp/papel: se generan dobles reservas, ausentismo sin recordatorios sistemáticos, tiempo de recepción confirmando manualmente y una ficha clínica desconectada de caja, obras sociales y liquidaciones (Discovery §1, §C3). Ningún producto local combina agenda multi-profesional/multi-sillón sin solapamientos + reserva 24/7 + WhatsApp nativo + odontograma + Mercado Pago + OS/prepagas con liquidaciones + facturación AFIP/ARCA + precio ARS transparente (Resumen ejecutivo, hallazgo 1).

## Objetivos por actor

| Actor | Objetivo principal | Objetivos secundarios |
|-------|--------------------|------------------------|
| Paciente | Reservar/reprogramar/cancelar online 24/7 viendo horarios libres reales | Recibir confirmación y recordatorios; pagar seña por Mercado Pago; consultar presupuesto |
| Odontólogo/a | Atender con agenda del día + ficha + odontograma + plan/presupuesto en la misma visita | Registrar evolución, consentimientos con firma, derivar a lista de espera |
| Recepcionista/secretaria | Dar de alta turnos con duración según prestación sin choques | Confirmar/reprogramar/cancelar, gestionar lista de espera, cobrar señas y caja diaria |
| Administrador/dueño | Liquidar por profesional y por OS/prepaga; ver reportes de facturación y ocupación | Gestionar roles, prestaciones, sillones, horarios, exportación de datos |

## Alcance v1 (MVP — Discovery §D3)

Imprescindibles (lo que SÍ hace v1):

- Agenda diaria/semanal multi-profesional + multi-sillón/box, duración variable por prestación, bloqueos, sobreturnos explícitos, anti-solapamiento por profesional Y por sillón (RN1–RN4).
- Reserva online 24/7 con link compartible (sin login obligatorio: nombre+DNI+teléfono), confirmación/cancelación/reprogramación + lista de espera básica.
- Recordatorios (al menos email + WhatsApp manual/planificado; automático como evolución).
- Ficha + anamnesis + odontograma básico (FDI, versionado) + presupuestos/planes de tratamiento.
- Caja + cobros + señas vía Mercado Pago + OS/prepagas + liquidaciones por profesional y por OS + reportes básicos.
- Roles/permisos, exportación de datos, trazabilidad de movimientos, soporte/capacitación inicial.
- Diferenciadores v1 si el alcance lo permite: turno que empieza justo cuando termina otro (borde permitido), lista de espera con reasignación, confirmación automática 24h.

## Fuera de alcance (explícitamente NO en v1 — roadmap posterior)

- Facturación electrónica AFIP/ARCA (Discovery: "No evidenciado" en locales; diseñar extensible).
- Periodontograma completo, imágenes/Rx, laboratorio radiológico.
- Portal del paciente con login, chatbot/IA recepcionista, recuperación de ausentes, campañas/membresías.
- Multi-sucursal avanzada, check-in QR, API pública, firma digital certificada.
- Integraciones fiscales de otros países (SII, NF-e, RIPS, CFDI) — solo referencia comparativa.

## Métricas de éxito

- Cero solapamientos persistidos por profesional o por sillón (violaciones bloqueadas = 100%).
- Reducción de ausentismo vs. línea base por recordatorios y confirmación 24h.
- Tiempo de alta de turno por recepción (< 2 min) y % de reservas online sobre total.
- Liquidaciones cerradas sin reclamos (conciliación profesional/OS cuadra con caja).
- Cobertura de tests por escenario del módulo de agenda (ver 08/09: API sin GUI obligatoria).
