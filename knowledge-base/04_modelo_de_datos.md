# Modelo de Datos

> Dominios derivados del MVP (Discovery §D3). Todos los datos de ejemplo son FICTICIOS (restricción Discovery §9).

## Dominios

- **Agenda**: profesionales, sillones/boxes, prestaciones, turnos, bloqueos, sobreturnos, lista de espera.
- **Pacientes y clínica**: pacientes, fichas/evoluciones, odontograma, consentimientos.
- **Administración**: presupuestos/planes, OS/planes, pagos/señas, caja, liquidaciones, reportes.
- **Transversal**: usuarios/roles, recordatorios, auditoría/trazabilidad.

## ERD (textual)

```
Profesional 1──N Turno N──1 Paciente 1──1 FichaClinica
Sillon     1──N Turno      Prestacion 1──N Turno (define duración RN3)
Turno 1──N Pago/Seña · Turno 1──N Recordatorio · Turno N──1 Presupuesto
Presupuesto N──1 ObraSocial/Plan · Liquidación N──N Turnos/Pagos
Paciente 1──N Consentimiento · Profesional 1──N Bloqueo (horario/feriado)
ListaEspera N──1 Paciente, Profesional, Prestación
Usuario N──1 Rol · Auditoría N──1 Usuario/Entidad (quién creó/movió/canceló/cobró)
```

## Entidades

### Paciente
- Atributos: id, nombre, dni (único), teléfono, email, fecha_nac, os_id + plan (nullable), notas. FICTICIO.
- Relaciones: 1──N Turnos, 1──1 Ficha, 1──N Consentimientos, 1──N Presupuestos.
- Constraints: dni único; teléfono obligatorio para reserva pública. Índices: dni, teléfono.

### Profesional
- Atributos: id, nombre, matrícula, especialidades[], horario_semanal (JSON), activo.
- Relaciones: 1──N Turnos, 1──N Bloqueos. Constraints: matrícula única.

### Sillon (box)
- Atributos: id, nombre/box, sucursal_id (reservado extensible, default "mono"), activo.
- Relaciones: 1──N Turnos. Constraints: nombre único por sucursal.

### Prestacion
- Atributos: id, nombre, duracion_min (RN3), precio_base, requiere_sillon (bool, default true), color_agenda.
- Relaciones: 1──N Turnos. Constraints: duracion_min > 0.

### Turno (entidad central)
- Atributos: id, paciente_id, profesional_id, sillon_id, prestacion_id, inicio (tz America/Argentina/Buenos_Aires), fin (= inicio + duración prestación, RN3), origen (mostrador/online), estado (reservado/confirmado/atendido/cancelado/ausente/sobreturno), token_publico, seña_id (nullable), os_aplicada (nullable).
- Relaciones: N──1 cada FK; 1──N Pagos, Recordatorios.
- Constraints: **fin > inicio; solapamiento prohibido por profesional (RN1) y por sillón (RN2)** — intervalos `[inicio, fin)`; borde `fin == inicio` siguiente PERMITIDO; sobreturno solo con flag explícito + rol autorizado. Índices: (profesional_id, inicio, fin), (sillon_id, inicio, fin).

### Bloqueo
- Atributos: id, profesional_id (nullable = general), sillon_id (nullable), desde, hasta, motivo (feriado/vacaciones/mantenimiento). Bloquea disponibilidad como intervalo ocupado.

### ListaEspera
- Atributos: id, paciente_id, profesional_id (nullable), prestacion_id, preferencia_horaria, estado (pendiente/reasignado/cancelado), creado_en.

### FichaClinica / Evolucion
- Atributos: id, paciente_id, profesional_id, fecha, anamnesis, evolución, adjuntos_ref (Rx post-MVP por referencia).

### Odontograma
- Atributos: pieza (FDI 11–48), estado (18 estados tipo DentalSoft: sano, caries, obturación, corona, endodoncia, extracción indicada, etc.), fecha, version (historial versionado). Clave: (paciente_id, pieza, version).

### Presupuesto / PlanTratamiento
- Atributos: id, paciente_id, items[] (prestación + cantidad + precio), os_id/plan + cobertura_aplicada (RN6), total, pagado, estado (borrador/aprobado/rechazado/en_curso).

### ObraSocial (OS/prepaga + plan)
- Atributos: id, nombre, plan, cobertura_reglas (JSON), activa.

### Pago / Seña
- Atributos: id, turno_id, medio (mercadopago/efectivo/transferencia), monto, estado (pendiente/aprobado/rechazado/devuelto), mp_payment_id, creado_por.

### Liquidacion
- Atributos: id, tipo (profesional/os), beneficiario_id, periodo, turno_ids[], total, estado (borrador/cerrada), pdf_ref.

### Usuario / Rol
- Atributos: id, nombre, email único, hash_password, rol (admin/recepcionista/odontologo), activo.

### Consentimiento
- Atributos: id, paciente_id, tipo, texto_version, firma_ref (RN6; digital certificada post-MVP), fecha.

### Recordatorio
- Atributos: id, turno_id, canal (email/whatsapp), programado_para, enviado_en, estado.

### Auditoria
- Atributos: id, fecha, usuario_id, entidad, entidad_id, accion (crear/mover/cancelar/cobrar/liquidar), detalle. Base de trazabilidad (RN6) y de la futura auditoría formal (ver 10).

## Seed data inicial (FICTICIA)

- Roles: admin, recepcionista, odontologo. Usuario admin inicial.
- 2 profesionales ficticios, 2 sillones (Box 1/2), 5 prestaciones (limpieza 30', consulta 20', obturación 45', endodoncia 90', ortodoncia control 30').
- OS ficticias: "OS Ejemplo Salud" (Plan Básico/Total), "Prepaga Ficticia" (Plan Uno).
- 3 pacientes ficticios, 4 turnos de ejemplo sin choques, 1 bloqueo de feriado, 1 item en lista de espera.
