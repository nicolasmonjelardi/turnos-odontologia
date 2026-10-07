# Actores y Roles

> Fuente: Discovery §2 (usuarios/roles) + casos de uso §3. Escala: mono-consultorio día 1 con modelo extensible a multi-sucursal (ver 10).

## Actores del sistema

| Actor | Descripción | Cómo interactúa |
|-------|-------------|-----------------|
| Paciente (externo, sin login obligatorio) | Persona que reserva atención; se identifica con nombre + DNI + teléfono | Link público 24/7: consulta disponibilidad, reserva, confirma, cancela, reprograma, paga seña |
| Recepcionista / secretaria | Gestiona agenda, confirmaciones, caja y señas | API autenticada: alta/edición de turnos, lista de espera, cobros, recordatorios |
| Odontólogo/a | Profesional que atiende y registra clínica | API autenticada: agenda del día, ficha/evolución, odontograma, planes/presupuestos, consentimientos |
| Administrador / dueño | Responsable de configuración, liquidaciones y reportes | API autenticada: ABM profesionales/sillones/prestaciones/OS, liquidaciones, reportes, roles, exportación |

## RBAC — Matriz de permisos

| Recurso | Paciente (público) | Recepcionista | Odontólogo/a | Administrador |
|---------|:---:|:---:|:---:|:---:|
| Disponibilidad / reserva online | R, crear propio | R/W | R | R/W |
| Turnos (todos) | R propio / cancelar propio | CRUD | R (los propios) + evolución | CRUD |
| Lista de espera | anotarse | CRUD + reasignar | R | CRUD |
| Pacientes / fichas | — | R/W datos contacto | R/W clínica | R/W |
| Odontograma | — | R | R/W | R |
| Presupuestos / planes | R propio | R/W | R/W | R/W |
| Pagos / señas / caja | pagar propio | R/W | R | R/W |
| OS / liquidaciones | — | R | R | R/W |
| Profesionales / sillones / prestaciones / bloqueos | — | R | R | R/W |
| Reportes / exportación | — | R básicos | R propios | R/W total |
| Usuarios / roles | — | — | — | R/W |

## Rutas públicas

Sin autenticación (identidad mínima nombre+DNI+teléfono, recomendación Discovery §11):

- `GET /disponibilidad` — consulta de horarios libres reales.
- `POST /turnos` (origen público) — crea reserva propia.
- `GET /turnos/:token` — ver/cancelar/reprogramar turno propio (token por reserva).
- `POST /pagos/seña` + webhook Mercado Pago — pago de seña del propio turno.
- `GET /presupuestos/:token` — ver presupuesto propio.
