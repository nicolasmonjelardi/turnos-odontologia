# Preguntas Abiertas

> Mode A: sin preguntas al usuario; las dudas quedan registradas aquí (discovery dejó estos puntos como "No evidenciado" — nunca completados por deducción).

## Inconsistencias detectadas

### IN-01 — Precio Dentatools (AJ-02 / V2)
**Documento A dice**: el informe final fija precio único $30.000 (hasta 3 prof.) + $8.000 extra, sin planes.
**Documento B dice**: borradores previos mencionaban un plan "Inicial $15.000".
**Impacto**: bajo (referencia comparativa, no afecta MVP). **Resolución propuesta**: vale el precio verificado V2; no usar el plan $15.000.

### IN-02 — OdontoSoft Millennium: reserva online (AJ-01)
**Documento A dice**: "No cuenta con reserva online (Comprobado)" — escritorio sin turnero.
**Documento B dice**: matriz anterior lo marcaba "No evidenciado".
**Impacto**: bajo. **Resolución propuesta**: vale AJ-01 (Comprobado); no contarlo como referencia de reserva online.

## Preguntas abiertas (priorizadas)

| Prioridad | Pregunta | Bloquea | Decisor |
|-----------|----------|---------|---------|
| Alta | Alcance MVP: ¿solo turnos+agenda o también clínica? (recomendado: incluir odontograma básico) | Sprint 1 | Cátedra / equipo |
| Alta | ¿Mono-consultorio o multi-sucursal día 1? (recomendado: mono extensible) | Modelo de datos | Equipo |
| Alta | Paciente: ¿login o solo nombre+DNI+teléfono? (recomendado: sin login) | Auth pública | Equipo |
| Media | **AFIP/ARCA — No evidenciado**: ningún local demuestra facturación electrónica integrada. ¿Alcance fiscal de v2 (solo comprobantes vs. liquidación completa)? | Roadmap fiscal | Equipo + contador |
| Media | **Periodontograma — No evidenciado** (DentalSoft, FLAP, Dentatools, AgendaPro, DenPro). ¿Clonar modelo de Dentalink/NovusOral en v2 o basta odontograma? | Roadmap clínico | Odontólogo referente |
| Media | **Auditoría formal — No evidenciado** en locales (exportación/auditoría formal ausente). ¿Qué nivel exige la cátedra: log consultable (v1) vs. pista firmada/exportable (v2)? | Cierre v1 | Cátedra |
| Media | **API pública — No evidenciado** en locales (solo ref. NexHealth `available_slots`+webhooks). ¿El contrato interno v1 debe congelarse como futura API pública? | Diseño API | Equipo |
| Media | WhatsApp 100% automático: ¿con qué BSP y a qué costo por mensaje en ARS? | Recordatorios auto | Admin |
| Baja | ~~Stack final: ¿Node o Python? (KB propone Node; Python es equivalente válido — DD-01)~~ **DECIDIDA 2026-10-07**: Python + FastAPI + SQLAlchemy + PostgreSQL + Redis + Docker / React + TypeScript + Vite (DD-01; tests backend pytest+httpx) | Sprint 1 | Equipo |
| Baja | [DISCOVERY] `scale` confirmado como equipo mono-consultorio; validar antes de multi-sucursal. | Roadmap | Equipo |

## Registro de verificación (trazabilidad Discovery)

- V1 DentalSoft, V3 Dentalink, V4 OdontoSoft, V5 Doctoralia, V6 Boreal: corregidos/verificados OK.
- V2 Dentatools: precio parcialmente inventado → corregido (IN-01).
- H1 Nimu→Nimbo, H2 Boreal (financiador, no software), H3 precios Dentalink/AgendaPro AR (cotización, no públicos): documentados en informe §Verificación.

## Preguntas resueltas

- 2026-10-07 — Stack final (era prior. Baja): decidido Python + FastAPI + SQLAlchemy + PostgreSQL + Redis + Docker / React + TypeScript + Vite; tests backend pytest + httpx. Ver DD-01, DD-05, DD-06 en 09.
