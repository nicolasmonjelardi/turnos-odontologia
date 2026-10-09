# agenda/crear-turno Specification

## Purpose

Permitir crear un turno de agenda calculando su fin por prestación y garantizando que no se solape por profesional ni por sillón, con borde semiabierto y hora AR bien definida.

## Requirements

### Requirement: Crear turno válido persiste reservado con auditoría
El sistema SHALL persistir un turno válido en estado `reservado` con `fin` calculado por prestación y registrar una entrada de auditoría append-only con quién/cuándo/qué.

#### Scenario: Turno feliz persiste reservado más auditoría
- **GIVEN** no existe turno para el profesional P ni para el sillón S en `[10:00, 10:30)` y existe una prestación de 30 min
- **WHEN** se envía `POST /api/turnos` con profesional P, sillón S, prestación de 30 min e `inicio` 10:00 válido en `America/Argentina/Buenos_Aires`
- **THEN** responde `201` con el turno en `reservado`, `fin = inicio + prestacion.duracion_min`, y existe una entrada de auditoría de creación

#### Scenario: Fecha ambigua o fin inválido se rechaza
- **GIVEN** una prestación válida y zona `America/Argentina/Buenos_Aires`
- **WHEN** se envía `POST /api/turnos` con fecha ambigua/inexistente en `America/Argentina/Buenos_Aires` o `fin <= inicio`
- **THEN** responde `422` y no persiste ningún turno ni auditoría de creación

### Requirement: Anti-solapamiento por profesional y por sillón con 409 identificado
El sistema SHALL rechazar con `409` toda creación que solape `[inicio, fin)` con un turno existente del mismo profesional o del mismo sillón, identificando el recurso en conflicto.

#### Scenario: Solapamiento por profesional devuelve 409
- **GIVEN** un turno existente del profesional P en `[10:00, 10:30)`
- **WHEN** se envía `POST /api/turnos` para P en `[10:15, 10:45)`
- **THEN** responde `409` con código `PROFESIONAL_OCUPADO` e identifica el turno existente, sin persistir nada

#### Scenario: Solapamiento por sillón devuelve 409 aunque el profesional esté libre
- **GIVEN** un turno existente en el sillón S en `[10:00, 10:30)` con otro profesional
- **WHEN** se envía `POST /api/turnos` en S en `[10:15, 10:45)` con un profesional libre
- **THEN** responde `409` con código `SILLON_OCUPADO` e identifica el turno existente, sin persistir nada

### Requirement: Borde fin igual a inicio permitido e intervalos semiabiertos
El sistema SHALL tratar los turnos como `[inicio, fin)`: un turno que empieza exactamente cuando termina otro no solapa y debe aceptarse.

#### Scenario: Turno que empieza justo cuando termina otro es válido
- **GIVEN** un turno existente para el mismo profesional y sillón en `[10:00, 10:30)`
- **WHEN** se envía `POST /api/turnos` para el mismo profesional y sillón en `[10:30, 11:00)`
- **THEN** responde `201` con el nuevo turno en `reservado`

### Requirement: Duración variable por prestación
El sistema SHALL calcular `fin = inicio + prestacion.duracion_min` y revalidar RN1+RN2 con ese fin; cambiar de prestación cambia el intervalo evaluado.

#### Scenario: Prestación más larga detecta choque que la corta no ve
- **GIVEN** un turno existente en `[11:00, 11:30)` y dos prestaciones candidatas desde `10:45` (una de 20 min, una de 15 min)
- **WHEN** se envía `POST /api/turnos` desde `10:45` con la prestación de 20 min (`fin 11:05`) y luego con la de 15 min (`fin 11:00`)
- **THEN** el de 20 min recibe `409` y el de 15 min recibe `201` (borde `fin == inicio` permitido)
