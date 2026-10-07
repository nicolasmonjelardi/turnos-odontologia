# Flujos Principales

> Todos los flujos corren sobre la API sin GUI obligatoria (ver 02/08). Huso horario `America/Argentina/Buenos_Aires` (RN10).

## Flujo 1: Crear un turno evitando solapamientos (change recomendado por la cátedra)
**Disparador**: recepcionista o paciente pide un slot. **Actor**: recepción / paciente (público).
**Pasos**:
1. Cliente pide `GET /disponibilidad` (profesional, sillón, prestación, rango) → API calcula slots con duración RN3 menos turnos/bloqueos.
2. Cliente envía `POST /turnos` (ids + inicio) → API calcula `fin`, valida RN1 (profesional) y RN2 (sillón) como intervalos `[inicio, fin)`.
3. Si choca → 409 con conflicto (profesional/sillón + turno existente). Si pasa → persiste `reservado` + entrada de auditoría.
4. Si exige seña (RN5) → genera link MP; webhook acredita → `confirmado`.
**Secuencia**: `Actor → API → DominioAgenda.valida(RN1+RN2) → Repo (PostgreSQL/SQLAlchemy) → Auditoría → respuesta`
**Casos de error**: choque profesional → 409 `PROFESIONAL_OCUPADO`; choque sillón → 409 `SILLON_OCUPADO`; fin inválido → 422; seña impaga vencida → libera slot + avisa lista de espera.

## Flujo 2: Reserva online 24/7 (público sin login)
**Disparador**: paciente abre el link. **Actor**: paciente.
**Pasos**: 1. Consulta disponibilidad → 2. Ingresa nombre+DNI+teléfono (RN12) → 3. Reserva (Flujo 1) → 4. Recibe token + confirmación WA/email → 5. Paga seña si aplica.
**Casos de error**: DNI/teléfono inválido → 422; slot tomado entre consulta y reserva → 409 + slots alternativos.

## Flujo 3: Confirmación / cancelación / reprogramación
**Disparador**: paciente o recepción. **Pasos**: 1. Valida antelación RN4 → 2a. Confirma (recordatorio 24h) / 2b. Cancela (libera slot → ofrece a lista de espera, RN5 si hay seña) / 2c. Reprograma atómico (RN9).
**Casos de error**: fuera de antelación → 422 + requiere rol; reprogramación con choque → 409 y se conserva el original.

## Flujo 4: Atención clínica (odontólogo)
**Disparador**: paciente presente. **Pasos**: 1. Agenda del día → 2. Ficha/evolución → 3. Odontograma versionado → 4. Plan/presupuesto con OS (RN6a) → 5. Consentimiento con firma (RN6c) → 6. Marca `atendido`.
**Casos de error**: sin consentimiento firmado → bloquea cierre de plan invasivo.

## Flujo 5: Caja, seña MP y liquidación
**Disparador**: cobro o cierre de período. **Pasos**: 1. Cobro/seña (MP webhook o manual) → 2. Asiento trazable (RN6b) → 3. Cierre: liquidación por profesional y por OS → 4. Reportes ocupación/facturación.
**Casos de error**: webhook duplicado → idempotencia por `mp_payment_id`; anulación → contra-asiento auditado, nunca borrado.

## Flujo 6: Lista de espera inteligente (diferenciador)
**Disparador**: cancelación. **Pasos**: 1. Slot liberado → 2. Busca candidatos compatibles → 3. Aviso WA/email → 4. Reasignación con validación RN1+RN2.
**Casos de error**: dos candidatos al mismo slot → primero que confirma gana, otro vuelve a espera.
