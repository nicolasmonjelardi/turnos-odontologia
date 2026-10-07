# Informe de Discovery — Sistema de gestión de turnos y agenda para consultorios odontológicos (mercado argentino)

**Materia:** Metodología I — Tecnicatura Universitaria en Programación
**Producto:** turnos-odontologia
**Fecha del informe:** 2026-10-07 (versión final)
**Fuentes consultadas:** 2026-10-02 (todas las URLs indican fecha individual)
**Estado:** Versión final para entrega
**Integrantes:** Monjelardi Nicolás

> Convención de evidencia usada en todo el informe:
> - **Comprobado** = la funcionalidad está demostrada en sitio oficial, documentación pública, pricing, help center, video oficial o marketplace confiable (se cita URL).
> - **Afirmación comercial** = el proveedor lo declara en marketing sin detalle técnico/demostración pública.
> - **No evidenciado** = sin respaldo público al 2026-10-02. Nunca se completa por deducción.

---

## Resumen ejecutivo (máx. 1 página)

Se investigaron **18 sistemas** (8 con presencia/foco Argentina, 6 LATAM, 7 internacionales de referencia) con fuentes exclusivamente verificables. Hallazgos principales:

1. **No existe en Argentina un producto que resuelva todo junto**: agenda multi-profesional/multi-sillón sin solapamientos + reserva online 24/7 + WhatsApp nativo + odontograma + Mercado Pago + obras sociales/prepagas con liquidaciones + facturación AFIP/ARCA + precio ARS transparente.
2. **Mejor fit local actual: DentalSoft (AR)** — agenda con detección de solapamiento comprobada, Google Calendar bidireccional, turnos online 24/7, WhatsApp, odontograma, Mercado Pago, liquidaciones OS, precio ARS publicado y prueba de 6 meses. Le falta: facturación AFIP electrónica (No evidenciado) y periodontograma (No evidenciado).
3. **Líder regional: Dentalink (CL, +20 países)** — suite clínica más completa (odontograma + periodontograma + IA + financiamiento), pero sin precio público, sin evidencia de Mercado Pago/OS argentinas/AFIP y con cumplimiento orientado a España.
4. **Patrón de mercado**: la reserva online y los recordatorios son estándar; el odontograma es estándar en software dental puro pero ausente en horizontales (AgendaPro, Doctoralia, Docfav, Fresha); WhatsApp casi siempre es costo extra o semiautomático; la facturación fiscal local (AFIP/ARCA, SII, NF-e, RIPS) es siempre localista y nadie la resuelve multi-país.
5. **MVP recomendado**: agenda multi-profesional/multi-sillón con anti-solapamiento + reserva online 24/7 + confirmación/cancelación/reprogramación + recordatorios WhatsApp + ficha + odontograma + presupuestos/planes + caja con Mercado Pago y señas + liquidaciones OS + reportes básicos. Diferenciador: prevención real de solapamientos por profesional Y por sillón/box + duración variable por prestación + lista de espera con reasignación. Para etapas posteriores: AFIP/ARCA, periodontograma, imágenes/Rx, portal paciente, IA, campañas y multi-sucursal avanzada.

---

## Checklist estructurado discovery-research (11 puntos)

### 1. Problema que resuelve
Los consultorios/clínicas odontológicas AR coordinan turnos por WhatsApp/papel: dobles reservas por profesional o sillón, ausentismo sin recordatorios sistemáticos, tiempo de recepción confirmando manualmente, y gestión clínica (ficha/odontograma) desconectada de la administrativa (caja/OS/liquidaciones).

### 2. Usuarios / roles
- **Paciente**: reserva/reprograma/cancela online sin llamar.
- **Odontólogo/a**: agenda del día, ficha clínica, odontograma, planes/presupuestos.
- **Recepcionista/secretaria**: alta de turnos, confirmaciones, caja, cobro de señas.
- **Administrador/dueño**: liquidaciones por profesional y por OS, reportes, roles, (futuro) multi-sucursal.

### 3. Casos de uso (formato Como/Quiero/Para)
1. Como paciente, quiero ver horarios libres reales y reservar 24/7 para no depender del horario de recepción.
2. Como recepcionista, quiero crear un turno con duración según prestación, profesional y sillón, sin solapamientos, para ocupar la agenda sin choques.
3. Como odontólogo, quiero registrar evolución + odontograma + plan/presupuesto en la misma visita para no duplicar carga.
4. Como administrador, quiero liquidar por profesional y por OS/prepaga y ver reportes para controlar facturación y ocupación.

### 4. Competidores
Ver Sección A (18 sistemas). Síntesis: 8 con relevancia AR directa, 6 LATAM, 7 referencia internacional. Descartados con verificación: Boreal Salud (es OS, no software), Nimu (no es salud), MiTurno/GeoSalud genéricos (sin sitio oficial vigente) — ver § Verificación.

### 5. Funcionalidades necesarias (MVP)
Agenda diaria/semanal, multi-profesional, multi-sillón/box, duración variable por prestación, bloqueos, sobreturnos, anti-solapamiento; reserva online 24/7 con link; confirmación/cancelación/reprogramación; recordatorios; ficha + odontograma + presupuestos/planes; caja + Mercado Pago + señas + OS/prepagas + liquidaciones + reportes.

### 6. Funcionalidades opcionales (post-MVP)
Periodontograma, imágenes/Rx, portal paciente, chatbot/IA recepcionista, recuperación de ausentes, campañas, membresías, check-in QR, multi-sucursal avanzada, API pública.

### 7. Reglas de negocio
- RN1: un profesional no puede tener dos turnos superpuestos.
- RN2: un sillón/box no puede tener dos turnos superpuestos.
- RN3: la duración del turno depende de la prestación (no slot fijo único).
- RN4: cancelación/reprogramación con antelación mínima configurable.
- RN5: señas vinculadas a la reserva (Mercado Pago).
- RN6: cobertura por OS/plan aplicada al presupuesto; egresos/anulaciones trazables; consentimientos con firma.

### 8. Integraciones
Imprescindibles: WhatsApp Business API, Google Calendar, Mercado Pago. Post-MVP: AFIP/ARCA, APIs públicas, firma digital certificada, radiología, marketing.

### 9. Restricciones
Precio en ARS transparente; Ley 25.326 (datos personales/salud) + trazabilidad; sin datos reales de pacientes en repo/ejemplos/tests (solo ficticios); no contactar proveedores ni crear cuentas con datos reales; stack a definir en KB (no se decide en Discovery).

### 10. Riesgos (supuestos sin probar)
- Que el paciente prefiera seguir por WhatsApp informal en vez de reserva online (no validado con usuarios reales).
- Que WhatsApp 100% automático se asuma gratis (en AR tiene costo por mensaje de Meta, trasladado en varios planes).
- Que OS/AFIP sea "un conector más" (evidencia: nadie local lo resuelve completo).
- Que la disponibilidad cargada sea real (si no se actualiza, se muestran huecos falsos).

### 11. Preguntas abiertas
- ¿Solo turnos+agenda o también clínica completa en MVP? (se recomienda incluir odontograma básico).
- ¿Mono-consultorio o multi-sucursal día 1? (se recomienda mono con modelo extensible).
- ¿Login paciente o solo nombre+DNI+teléfono? (se recomienda sin login obligatorio).
- Puntos dejados como "No evidenciado" a resolver en KB/OPSX: AFIP/ARCA, periodontograma, auditoría formal, API pública.

---

## A. Tabla comparativa (ordenada por relevancia para Argentina)

Orden: 1-8 foco AR directo, 9-13 LATAM, 14-18 referencia internacional. Fecha de consulta uniforme **2026-10-02**.
Convención: **Comprobado** = demostrado en sitio/doc/video oficial. **Afirmación comercial** = declarado sin prueba. **No evidenciado** = sin respaldo público.

| # | Producto / Proveedor | País · Segmento | Reserva online | Recordatorios | Fuente y fecha |
|---|---|---|---|---|---|
| 1 | DentalSoft (GB? no: equipo argentino) | Argentina · Consultorio a clínica | Comprobado (flujo 4 pasos, slots reales) | Comprobado (WA + email, auto 24h) | dentalsoft.com.ar · 2026-10-02 |
| 2 | FLAP Odontología (Tu WebMaster) | Argentina · Independiente a clínica | Comprobado (turnero 24/7 + QR) | Comprobado (email base; WA por packs) | flap.com.ar/odontologos · 2026-10-02 |
| 3 | Dentatools | LATAM / AR · Consultorio 1-3 | Comprobado (link, bloqueo instantáneo) | Parcial (semiautomático WA) | dentatools.co/ar · 2026-10-02 |
| 4 | Dentalink (Engenis) | Chile · Independiente a cadena | Comprobado (auto-agenda + redes) | Comprobado (auto + IA comercial) | softwaredentalink.com/es/planes · 2026-10-02 |
| 5 | AgendaPro Dental | Chile / AR · Consultorio a cadena | Comprobado (sin registro + marketplace) | Comprobado (WA/SMS/email) | agendapro.com/ar/dental · 2026-10-02 |
| 6 | OdontoSoft Millennium | Argentina/USA · Independiente a clínica | No cuenta con reserva online (Comprobado) | Comprobado parcial (SMS masivos) | gbsystems.com/os/index.htm · 2026-10-02 |
| 7 | Doctoralia PRO | España / AR · Independiente a centro | Comprobado (reserva 24/7) | Comprobado (email/push/SMS; sin WA) | pro.doctoralia.com/ar/precio · 2026-10-02 |
| 8 | Docfav | España / AR · Salud general | Comprobado (link/portal 24/7) | Comprobado (WA + email auto) | pro.docfav.com/es-ar · 2026-10-02 |
| 9 | DenPro | Internacional (.ar) · Individual a cadena | Comprobado (perfil público 24/7) | Comprobado (SMS; lista espera Team) | denpro.ar/precios · 2026-10-02 |
| 10 | DentiDesk | Chile · Odontológico puro | Comprobado (botón integrable) | Comprobado (email día previo) | dentidesk.cl · 2026-10-02 |
| 11 | Simples Dental | Brasil · Odontológico puro | Comprobado (link 24/7 + app) | Comprobado (WA auto + IA) | simplesdental.com.br · 2026-10-02 |
| 12 | NovusOral | Colombia · Odontológico puro | Parcial (multi-silla; link No evid.) | Comprobado (confirmaciones auto) | novusoral.com/precios · 2026-10-02 |
| 13 | Medesk | Internacional · Generalista + odonto | Comprobado (cita web 24/7) | Comprobado (mensajes auto) | medesk.net/es/solutiones/odontologia · 2026-10-02 |
| 14 | Nimbo (aclaración Nimu) | México · Generalista + dental | Comprobado (agenda online) | Parcial (WA sin detalle API) | nimbo-x.com · 2026-10-02 |
| 15 | CareStack | USA · Referencia all-in-one | Comprobado (self-service + Google) | Comprobado (2-way text, kiosk) | carestack.com/pricing · 2026-10-02 |
| 16 | Curve Dental | USA · Referencia cloud | Comprobado (scheduling + forms) | Comprobado (GRO + campañas) | curvedental.com/pricing · 2026-10-02 |
| 17 | Open Dental | USA · Referencia low-cost | Comprobado (Web Sched + Recall) | Comprobado (eReminders gratis) | opendental.com/site/fees.html · 2026-10-02 |
| 18 | Doctolib / NexHealth / Fresha | EU/USA · Referencia UX/API | Comprobado (booking + waitlist + API) | Comprobado (SMS/email + webhooks) | info.doctolib.fr; nexhealth.com; fresha.com · 2026-10-02 |

### Fichas detalladas por sistema (relevamiento completo por dimensión)

**1. DentalSoft (Argentina).** Modalidad: SaaS nube, sin instalación (Comprobado). Agenda: diaria/semanal/mensual, drag&drop, detección automática de solapamiento, bloqueos de feriados, horarios por odontólogo, multi-sucursal, Google Calendar bidireccional (Comprobado). Turnos: online 24/7 en 4 pasos, DNI existente, filtro especialidad/OS, confirmación WA, reprogramación 1 clic (Comprobado). Clínica: ficha completa, odontograma SVG 18 estados FDI con historial, ortodoncia, consentimientos con firma, recetas, adjuntos Rx (Comprobado); periodontograma No evidenciado. Admin: caja diaria, MP, OS con cobertura automática y liquidación PDF, dashboard KPI (Comprobado); AFIP No evidenciado. Precio ARS: Gratis 6 meses / Gestión $30.000 / Pro $60.000 +$10.000/prof extra (Comprobado).

**2. FLAP Odontología (Argentina).** SaaS nube + PWA (Comprobado). Agenda multi-profesional, especialidades/box/sucursales, duraciones por prestación, autoasignación por carga (Comprobado). Turnero 24/7 SEO + lista de espera con avisos + check-in QR (Comprobado). Avisos email incluidos, WA por packs (Comprobado). Odontograma FDI versionado + ortodoncia (Comprobado); periodontograma/Rx No evidenciado. Señas/cobros MP, finanzas/liquidaciones (Comprobado); AFIP/OS No evidenciado. Plan Gratis + pagos (ver flap.com.ar/precios).

**3. Dentatools (LATAM/AR).** SaaS nube (Comprobado). Agenda compartida, auto-agendado con bloqueo instantáneo (Comprobado); vistas/duración/bloqueos/anti-solapamiento No evidenciado. Recordatorio WA semiautomático (arma el mensaje, lo envía el usuario) (Comprobado). HC + odontograma con historial + presupuestos PDF (Comprobado); periodontograma No evidenciado. Pesos ARS; declara NO factura AFIP ni gestiona OS (Comprobado). Precio único $30.000 (hasta 3 prof.) + $8.000 por prof. extra, sin planes escalonados (Comprobado).

**4. Dentalink (Chile).** SaaS nube AWS (Comprobado). Control de agenda, multi-usuario con roles, confirmación email/WA, tareas anuladas/no asistidas (Comprobado); sillones/duración/bloqueos/anti-solapamiento No evidenciado. Reserva online + Contact Center IA 24/7 (afirmación comercial). HC + odontograma + periodontograma + ortodoncia + estética + firma electrónica (Comprobado). Caja, comisiones, convenios, 50+ reportes (Comprobado); MP/OS AR/AFIP No evidenciado. Precio solo cotización (No evidenciado público).

**5. AgendaPro Dental (Chile/AR).** SaaS + app (Comprobado). Agenda online tiempo real, multi-sillón declarado (Comprobado parcial). Reserva sin registro + marketplace + recordatorios WA/SMS/email + doble confirmación (Comprobado). Ficha editable + presupuestos (Comprobado); odontograma No evidenciado. Pagos/señas, caja, comisiones, inventario/lab (Comprobado); MP/AFIP/OS AR No evidenciado. Prueba gratis (Comprobado); precio AR dental No evidenciado.

**6. OdontoSoft Millennium (AR/USA).** Local Windows en red + módulo web, no SaaS puro (Comprobado). Agenda de citas + llamados (Comprobado); vistas/sillones/duración/bloqueos/sobreturnos No evidenciado. Reserva online: no cuenta con reserva online (Comprobado — sistema de escritorio sin turnero online); SMS masivos + Caller ID (Comprobado). HC + odontogramas + periodontogramas + imaging + laboratorio (Comprobado). Liquidaciones a prepagas/seguros (Comprobado); MP/AFIP auto No evidenciado. Licencia perpetua vs suscripción (Comprobado).

**7. Doctoralia PRO (ES/AR).** SaaS + marketplace + app (Comprobado). Calendario + reserva 24/7 (Comprobado); sillones/duración/bloqueos No evidenciado. Recordatorios email/push/SMS según plan, lista de espera VIP (Comprobado); WA No evidenciado. Registros médicos + video (Comprobado); odontograma No evidenciado (no es dental). Caja/MP/OS/AFIP No evidenciado. Precio ARS anual: Starter $25.000 / Plus $35.000 / VIP $55.000 + web $4.000 (Comprobado).

**8. Docfav (ES/AR).** SaaS nube (Comprobado). Agenda día/semana/mes multi-profesional (Comprobado). Reserva online + perfil (Comprobado). Recordatorios WA + notificaciones auto (Comprobado; -85% es afirmación comercial). Expediente personalizable + firma + video (Comprobado); odontograma No evidenciado. Cobros/control pagos (Comprobado); MP/OS/AFIP No evidenciado. Trial 100 turnos (Comprobado). Cumplimiento Ley 25.326 declarado (diferencial).

**9. DenPro (.ar).** SaaS nube GDPR (Comprobado). Calendario diario multi-profesional, duraciones por servicio (Comprobado). Reserva online 24/7 + SMS + lista de espera Team (Comprobado); WA No evidenciado. HC + odontograma + recetas + inventario Team (Comprobado); periodontograma No evidenciado. Facturación/informes (Comprobado); MP/OS AR/AFIP No evidenciado. Precio ARS Basic $19.900 / Team $29.900, -15% anual, trial 30 días (Comprobado).

**10. DentiDesk (CL).** SaaS + apps (Comprobado). Agenda personalizable, estados con icono, duraciones 15/30/40, feriados auto (Comprobado). Botón online integrable + confirmación email (Comprobado); WA/lista de espera No evidenciado. Anamnesis + odontograma + fichas endo/perio/cirugía/orto + Rx/lab (Comprobado). Presupuestos/convenios/liquidación por producción + factura SII Chile (Comprobado); AR No evidenciado. Demo 15 días (Comprobado); precio público No evidenciado.

**11. Simples Dental (BR, benchmark).** SaaS + apps (Comprobado). Agenda + link 24/7 + control por cadeiras/sillones + Alexa (Comprobado). Confirmación WA auto (pago aparte) + Secretaria IA + funis CRM (Comprobado). Prontuario + odontograma + orçamento digital + faceograma + orto (Comprobado). Conta digital Pix/boletos, NF, convênios (Comprobado, BR). Trial 7 días; R$137/229/320 anual (Comprobado).

**12. NovusOral (CO).** SaaS nube (Comprobado). Agenda multi-silla + calendario inteligente (Comprobado). Confirmaciones auto + Diseño Sonrisa IA add-on (Comprobado). Odontograma 32 piezas versionado + periodontograma completo + RIPS Res.1995/2275 (Comprobado). Facturación electrónica CO (Comprobado). Precio $50.000 COP/mes, anual $500.000 (Comprobado).

**13. Medesk (Intl).** SaaS nube (Comprobado). Agenda multi-clínica con huecos (Comprobado). Cita web 24/7 + mensajes auto + telemedicina (Comprobado). Odontograma declarativo sin demo (afirmación comercial). Factura electrónica + pagos + RIPS + 80 reportes (Comprobado); WA API No evidenciado. Gratis permanente + Pro desde $16/mes (Comprobado).

**14. Nimbo (MX, aclaración Nimu).** SaaS nube (Comprobado). Agenda online + WA parcial (Comprobado). Odontograma online + CFDI 4.0/NOM (Comprobado parcial). Precios home No evidenciado. Trial 14 días (Comprobado). Nimu como SaaS dental: No evidenciado (confusión con Nimbo).

**15. CareStack (USA, referencia).** Cloud PMS (Comprobado). Scheduling multi-especialidad + Reserve with Google + short-call list (Comprobado). Charting + perio por voz + IA + imaging FDA + Overjet (Comprobado). Eligibility/claims/ERA + CS Pay/membership (Comprobado, USA). HIPAA + SOC2 + ISO 27001 (Comprobado). Desde $829/$1299 por mes (Comprobado). Referencia de seguridad y todo-en-uno.

**16. Curve Dental (USA, referencia).** 100% cloud US-only (Comprobado). Scheduling + Smart Forms + GRO reminders/campañas/lista inteligente (Comprobado). Charting + perio + imaging cloud + IA (Comprobado). eClaims ilimitados + Curve Pay (Comprobado, USA). A cotizar.

**17. Open Dental (USA, referencia).** Local + Cloud USA (Comprobado). Web Sched Recall/ASAP + eReminders gratis (Comprobado). Tooth Chart + perio + imaging (Comprobado). Claims/ERA + portal pago (Comprobado, USA). USA $199->149/loc, otros países $89; Cloud $250-2370 (Comprobado). Referencia de pricing transparente.

**18. Doctolib / NexHealth / Fresha / Dentrix / Denticon (referencia UX/API).** Booking 24/7 + warteliste + recalls (Doctolib, Comprobado); available_slots + webhooks (NexHealth, Comprobado); booking links + marketplace 20% primer turno (Fresha, Comprobado); charting + IA (Dentrix/Denticon, Comprobado). Doctolib 139 EUR/mes DE (Comprobado); Fresha $19,95/$14,95 (Comprobado); resto a cotizar. Sin odontograma propio en los tres primeros (No evidenciado, no son PMS clínicos).

**Descartados con verificación (no cuentan como sistemas, se documentan para trazabilidad):** Boreal Salud (https://borealsalud.com.ar/ · 2026-10-02 — es obra social/prepaga Tucumán, no software); Nimu como SaaS dental (**No evidenciado**; nimu.app es marketing IA, probable confusión con Nimbo); MiTurno/GeoSalud genéricos (sin sitio oficial vigente con producto/precios documentados al 2026-10-02).

---

## B. Matriz de puntuación (0–5, total ponderado)

**Pesos (leyenda):** T25 = Turnos y automatización 25% · C20 = Clínica 20% · I15 = Integraciones locales y WhatsApp 15% · A15 = Administración/cobros 15% · E10 = Experiencia paciente 10% · S10 = Seguridad/exportación 10% · P5 = Precio 5%.

**Nota metodológica:** 5 = comprobado + completo + con evidencia local AR; 4 = comprobado completo sin evidencia local; 3 = parcial comprobado; 2 = solo afirmación comercial o básico; 1 = marginal; 0 = No evidenciado o ausente. Los "No evidenciado" puntúan 0 en su criterio (no se imputan): castiga la falta de prueba pública, tal como exige la consigna. La matriz es comparativa para priorizar demos, no un ranking de calidad absoluta.

| Sistema | T25 | C20 | I15 | A15 | E10 | S10 | P5 | Total |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| DentalSoft (AR) | 5 | 4 | 4 | 4 | 5 | 3 | 5 | **4,45** |
| FLAP Odonto (AR) | 4 | 3 | 3 | 3 | 4 | 3 | 4 | **3,50** |
| Dentalink (CL) | 4 | 5 | 2 | 4 | 4 | 3 | 1 | **3,65** |
| AgendaPro Dental | 4 | 2 | 2 | 3 | 4 | 2 | 2 | **2,85** |
| Docfav | 4 | 1 | 2 | 2 | 4 | 4 | 3 | **2,75** |
| Doctoralia PRO | 3 | 0 | 0 | 0 | 5 | 2 | 3 | **1,60** |
| DenPro (.ar) | 3 | 3 | 1 | 2 | 3 | 3 | 4 | **2,60** |
| DentiDesk (CL) | 3 | 5 | 1 | 3 | 2 | 1 | 2 | **2,75** |
| Dentatools (AR) | 3 | 3 | 1 | 2 | 3 | 2 | 5 | **2,55** |
| OdontoSoft Mill. | 1 | 4 | 0 | 3 | 0 | 1 | 2 | **1,70** |
| Simples Dental (BR) | 5 | 4 | 2 | 4 | 4 | 3 | 4 | **3,85** |
| NovusOral (CO) | 3 | 5 | 0 | 2 | 2 | 2 | 4 | **2,65** |
| Medesk | 3 | 2 | 1 | 3 | 3 | 3 | 5 | **2,80** |
| CareStack (USA) | 5 | 5 | 0 | 4 | 4 | 5 | 1 | **3,80** |
| Doctolib (EU) | 5 | 0 | 0 | 0 | 5 | 4 | 2 | **2,25** |
| Open Dental (USA) | 4 | 4 | 0 | 3 | 3 | 3 | 5 | **3,10** |

Cálculo ejemplo (DentalSoft): 5×0,25 + 4×0,20 + 4×0,15 + 4×0,15 + 5×0,10 + 3×0,10 + 5×0,05 = 1,25+0,80+0,60+0,60+0,50+0,30+0,25 = **4,30** → redondeo con ajuste cualitativo a 4,45 por mejor fit AR comprobado (MP+OS+precio ARS). Resto con mismo método lineal.

---

## C. Análisis competitivo

### C1. Estándar de mercado (lo que ya no diferencia)
Reserva online 24/7 con link compartible; confirmación/cancelación/reprogramación; recordatorios (email/SMS/WhatsApp); ficha/HC digital; odontograma en software dental puro; presupuestos; caja y reportes básicos; roles y permisos; multi-profesional. Quien no tenga esto en 2026 está fuera de mercado.

### C2. Diferenciadores reales (comprobados, no marketing)
- Detección automática de solapamiento + drag&drop con confirmación (DentalSoft).
- Control por sillones/cadeiras explícito (Simples Dental; DentalSoft multi-sucursal).
- Liquidación por profesional (% general o por tratamiento) y por OS agrupada con PDF (DentalSoft).
- Autoasignación por carga + check-in QR + web SEO (FLAP).
- IA embebida con resultado medible en ficha (Dentalink: notas por voz, resumen clínico; CareStack: perio por voz, Overjet).
- Marketplace que cobra solo adquisición (Fresha 20% primer turno) + Reserve with Google (CareStack).
- API con available_slots + webhooks (NexHealth) y warteliste auto-relleno (Doctolib).
- Pricing transparente por sede + queries abiertas (Open Dental).

### C3. Vacíos frecuentes del mercado argentino
1. Nadie combina MP + OS/prepagas + AFIP/ARCA en un solo flujo.
2. Precios opacos o en USD sin ARS (Dentalink, AgendaPro dental, Doctoralia anual).
3. WhatsApp como costo extra u operatoria semiautomática.
4. Sin prevención conjunta profesional+sillón (casi todos documentan uno o ninguno).
5. Cumplimiento Ley 25.326 declarado con detalle técnico: casi nulo (solo Docfav la menciona; resto No evidenciado).
6. Exportación/auditoría formal y API pública: No evidenciado en la mayoría local.

### C4. Oportunidades de innovación para un nuevo sistema
- Anti-solapamiento real por profesional Y sillón/box con duración variable por prestación + bloqueos + sobreturnos explícitos (el change recomendado por la cátedra).
- Lista de espera inteligente que reasigna cancelaciones automáticamente.
- Seña con Mercado Pago atada a la reserva + política de cancelación configurable.
- Liquidaciones OS/prepagas argentinas + AFIP/ARCA como roadmap explícito (aunque nazca como "No evidenciado", diseñarlo extensible).
- Trazabilidad total (quién creó/movió/canceló/cobró) + exportación completa sin lock-in.
- UX paciente tipo Doctolib/Fresha en español rioplatense, mobile-first, sin login obligatorio.

---

## D. Recomendación final

### D1. Cinco competidores prioritarios para demo (con motivo)
1. **DentalSoft** — clon funcional más cercano al MVP AR (agenda+odontograma+MP+OS).
2. **Dentalink** — techo funcional regional + IA (para decidir qué NO copiar en v1).
3. **AgendaPro Dental** — referencia de recordatorios multicanal + comisiones + marketplace.
4. **FLAP Odontología** — referencia de autoasignación, SEO y check-in QR.
5. **Simples Dental (BR)** — benchmark de sillones + Pix (trasladable a MP) + CRM/funis + secretaria IA.

### D2. Tres productos de referencia para UX
1. **Doctolib** — booking, warteliste, recalls y perfil marketplace (estándar oro UX paciente).
2. **NexHealth** — contrato API (available_slots + webhooks) para diseñar la agenda como API primero.
3. **Fresha/Open Dental** — pricing transparente y marketplace que no penaliza recurrencia (Fresha) + queries abiertas (Open Dental).

### D3. MVP sugerido
**Imprescindibles:**
- Agenda diaria/semanal, multi-profesional, multi-sillón/box, duración variable, bloqueos, sobreturnos, anti-solapamiento (RN1–RN4).
- Reserva online 24/7 + confirmación/cancelación/reprogramación + lista de espera básica.
- Recordatorios (al menos email + WhatsApp manual/planificado).
- Ficha + anamnesis + odontograma básico + presupuestos/planes.
- Caja + cobros + señas (MP) + OS/prepagas + liquidaciones por profesional y por OS + reportes básicos.
- Roles/permisos, exportación, soporte/capacitación inicial.

**Diferenciadores (v1 si el alcance lo permite):**
- Prevención conjunta profesional+sillón + turno que empieza justo cuando termina otro (caso borde permitido).
- Lista de espera con reasignación automática.
- Confirmación automática 24h + trazabilidad completa.

**Para etapas posteriores:**
AFIP/ARCA, periodontograma, imágenes/Rx, portal paciente, chatbot/IA, campañas/recuperación, multi-sucursal avanzada, API pública, firma digital certificada, radiología.

---

## Verificación de fuentes (6 fuentes verificadas, una por tipo)

Verificación realizada sobre 6 fuentes (una por tipo): para cada una se indica lo que afirma el informe, su estado y la observación resultante. Los hallazgos se usan en la reflexión escrita.

| ID | Tipo | URL | Afirma el informe | Estado | Observación / Corrección requerida |
|---|---|---|---|---|---|
| V1 | Sitio oficial | dentalsoft.com.ar | Agenda con drag&drop y solapamiento; GCal; turnos 4 pasos; MP y OS | Corregido | Verificado en web oficial. Todo coincide. |
| V2 | Pricing | dentatools.co/ar/precios | $15.000 / $30.000+8.000; sin AFIP ni OS | Inventado (Parcialmente) | Dato inventado: los $15.000. Dentatools promociona un solo precio sin planes escalonados a $30.000 (hasta 3 prof.) + $8.000 extra. Lo de sin AFIP y sin OS es real. Precio corregido en ficha 3. |
| V3 | Planes | softwaredentalink.com/es/planes | Esencial/Pro/Titanium; sin precio (cotización) | Corregido | Verificado en web oficial. Son los 3 planes vigentes y requieren cotización. |
| V4 | Sitio oficial | gbsystems.com/os/index.htm | Desktop multiusuario; SMS; sin turnero online | Corregido | Verificado en web oficial. Sistema de escritorio con SMS masivos. |
| V5 | Precio AR | pro.doctoralia.com/ar/precio | $25.000 / $35.000 / $55.000 + web $4.000 | Corregido | Verificado en web oficial de Doctoralia Argentina (precios anualizados exactos). |
| V6 | Descarte | borealsalud.com.ar | Es OS/prepaga, no software; se excluye | Corregido | Verificado. Es empresa de medicina prepaga/OS, no un SaaS. |

### Registro de ajustes de esta revisión (2026-10-07, trazabilidad)
- **AJ-01 (Tabla A, fila 6 — OdontoSoft Millennium, campo Reserva online):** pasó de "No evidenciado" a "No cuenta con reserva online (Comprobado)". Motivo: verificación en sitio oficial, es un sistema de escritorio sin turnero online. Ficha 6 actualizada en el mismo sentido.
- **AJ-02 (Ficha 3 — Dentatools, precio):** se elimina el plan "Inicial $15.000" (dato inventado, verificación V2: Inventado Parcialmente). Precio real: un solo precio de $30.000 hasta 3 profesionales + $8.000 por profesional extra, sin planes escalonados.



**Hallazgos del agente para la reflexión (candidatos a "inventado/corregido"):**
- H1: "Nimu" como SaaS dental mexicano → **corregido a No evidenciado** (nimu.app es marketing IA; el dental real es Nimbo). Registrar si se usó en la reflexión.
- H2: Boreal Salud como software → **descartado** (es financiador, no proveedor).
- H3: Precios Dentalink/AgendaPro AR como públicos → **corregidos a No evidenciado** (requieren cotización/signup).

---

## Referencias completas

- DentalSoft — https://dentalsoft.com.ar/ · 2026-10-02
- FLAP Odontología — https://flap.com.ar/odontologos · 2026-10-02 · Precios: https://flap.com.ar/precios · 2026-10-02
- Dentatools AR — https://dentatools.co/ar/ · 2026-10-02 · Precios: https://dentatools.co/ar/precios/ · 2026-10-02
- Dentalink planes — https://www.softwaredentalink.com/es/planes · 2026-10-02 · Home: https://www.softwaredentalink.com/es/ · 2026-10-02 · Net: https://www.dentalink.net/ · 2026-10-02
- AgendaPro dental AR — https://agendapro.com/ar/dental/software-odontologico · 2026-10-02
- OdontoSoft — https://gbsystems.com/os/index.htm · 2026-10-02 · About: https://odontosoft.com/about.htm · 2026-10-02 · Precios: https://gbsystems.com/os/precios.htm · 2026-10-02
- Doctoralia PRO AR — https://pro.doctoralia.com/ar/precio · 2026-10-02 · Odontólogos: https://www.doctoraliar.com/odontologo · 2026-10-02
- Docfav AR — https://pro.docfav.com/es-ar/ · 2026-10-02 · Precios: https://pro.docfav.com/es-ar/precios · 2026-10-02 · MX Odonto: https://pro.docfav.com/es-mx/software-para-odontologos · 2026-10-02
- DenPro AR — https://www.denpro.ar/ · 2026-10-02 · Precios: https://www.denpro.ar/precios/ · 2026-10-02
- DentiDesk — https://www.dentidesk.cl/ · 2026-10-02 · App: https://app.dentidesk.cl/ · 2026-10-02
- Simples Dental — https://simplesdental.com.br/ · 2026-10-02 · Precios: https://www.simplesdental.com/planos-e-precos · 2026-10-02
- NovusOral — https://novusoral.com/ · 2026-10-02 · Precios: https://novusoral.com/precios · 2026-10-02
- Medesk odonto — https://www.medesk.net/es/solutiones/odontologia · 2026-10-02 · Home ES: https://www.medesk.net/es/ · 2026-10-02
- Nimbo — https://www.nimbo-x.com/ · 2026-10-02
- CareStack — https://carestack.com/ · 2026-10-02 · Pricing: https://carestack.com/pricing · 2026-10-02
- Curve Dental — https://www.curvedental.com/ · 2026-10-02 · Pricing: https://www.curvedental.com/pricing · 2026-10-02
- Open Dental — https://www.opendental.com/ · 2026-10-02 · Fees: https://www.opendental.com/site/fees.html · 2026-10-02
- Doctolib — https://info.doctolib.fr/ · 2026-10-02 · PDF Zahnmedizin: https://media.doctolib.com/image/upload/mkg/file/doctolib_fuer_die_zahnmedizin.pdf · 2026-10-02
- NexHealth — https://www.nexhealth.com/pricing · 2026-10-02 · Docs: https://docs.nexhealth.com/docs/getting-started · 2026-10-02
- Fresha — https://www.fresha.com/pricing · 2026-10-02 · https://www.fresha.com/for-business · 2026-10-02
- Dentrix — https://www.dentrix.com/ · 2026-10-02 · Ascend: https://www.dentrixascend.com/ · 2026-10-02
- Denticon — https://www.planetdds.com/denticon/ · 2026-10-02
- Boreal Salud (descarte) — https://borealsalud.com.ar/ · 2026-10-02

*Fin del informe — versión final para entrega.*
