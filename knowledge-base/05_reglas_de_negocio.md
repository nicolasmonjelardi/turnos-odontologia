# Reglas de Negocio

> Códigos `RN-XX` exigidos por la cátedra (corresponden a Discovery §7: RN1–RN6). Reglas extra del MVP se numeran RN7+.

## Dominio: Agenda (RN1–RN4, RN7–RN9)

- **RN1 — Sin solapamiento por profesional**: un profesional no puede tener dos turnos superpuestos. Intervalos `[inicio, fin)`; choque si `nuevo.inicio < existente.fin AND nuevo.fin > existente.inicio`. Borde permitido: `nuevo.inicio == existente.fin`.
- **RN2 — Sin solapamiento por sillón/box**: un sillón/box no puede tener dos turnos superpuestos (misma aritmética que RN1, evaluada en paralelo). Ambas validaciones deben pasar para persistir.
- **RN3 — Duración variable por prestación**: `turno.fin = turno.inicio + prestacion.duracion_min`. No existe slot fijo único; cambiar la prestación recalcula el fin y revalida RN1+RN2.
- **RN4 — Antelación mínima configurable**: cancelación/reprogramación solo hasta `X` horas antes (param. por consultorio, default 24h). Fuera de plazo → requiere rol admin/recepción + queda en auditoría.
- **RN7 — Bloqueos**: feriados, vacaciones y mantenimientos son intervalos ocupados que bloquean disponibilidad igual que un turno.
- **RN8 — Sobreturnos explícitos**: solo con flag `sobreturno=true` + rol autorizado (recepción/admin); se listan diferenciados y no cuentan como hueco.
- **RN9 — Reprogramación**: es cancelación + creación atómica bajo RN1+RN2; si el nuevo slot choca, la operación completa falla (409) y el turno original se conserva.

## Dominio: Pagos y señas (RN5)

- **RN5 — Señas vinculadas a la reserva (Mercado Pago)**: la reserva puede exigir seña; el turno queda `reservado` hasta acreditarse el pago (webhook MP) → pasa a `confirmado`. Devolución/compensación ante cancelación según política configurable.

## Dominio: Cobertura, trazabilidad y consentimiento (RN6)

- **RN6a — Cobertura por OS/plan**: el presupuesto aplica `os_id/plan` y sus reglas de cobertura; el monto a cargo del paciente = total − cobertura. Sin OS válida → particular.
- **RN6b — Egresos y anulaciones trazables**: todo movimiento de caja, anulación o devolución registra quién, cuándo y motivo en Auditoría; nada se borra físicamente.
- **RN6c — Consentimientos con firma**: cada plan invasivo requiere consentimiento versionado con firma registrada antes del `atendido`.

## Dominio: Excepciones globales

- **RN10 — Huso horario**: todos los turnos en `America/Argentina/Buenos_Aires`; la API rechaza fechas ambiguas/inválidas.
- **RN11 — Datos ficticios**: prohibido persistir o commitear datos reales de pacientes en repo, ejemplos, seeds o tests (restricción Discovery §9; Ley 25.326).
- **RN12 — Reserva pública mínima**: el canal público exige nombre + DNI + teléfono; no exige contraseña (decisión Discovery §11).
