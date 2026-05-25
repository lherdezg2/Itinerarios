# Itinerarios - MVP Academico

Proyecto base para Ingenieria de Software II con arquitectura de microservicios y arquitectura hexagonal.

## Estructura

- `airport-service`: microservicio de consulta de aeropuertos.
- `itinerary-service`: microservicio de gestion de itinerarios.
- `airport-map-web`: frontend estatico (mapa, seleccion, validacion cliente y creacion de itinerario).
- `docker-compose.yml`: levanta servicios, base de datos y mapa web.

## Arquitectura aplicada

Cada microservicio usa:

- `domain`: entidades y reglas de negocio.
- `application/ports`: interfaces de entrada y salida.
- `application/use_cases`: implementacion de casos de uso.
- `adapters/inbound/rest`: controladores HTTP.
- `adapters/outbound/*`: acceso externo (DB o API).

Regla clave: el dominio no depende de Django, ORM, REST ni clientes externos.

## Levantar el proyecto

Requisito: Docker Desktop instalado.

```bash
docker compose up --build
```

Servicios:

- Airport Service: http://localhost:8001/api/airports/
- Itinerary Service: http://localhost:8002/api/itineraries/
- Mapa web (HU-A3+): http://localhost:8080/

## Endpoints base MVP

Airport Service:

- `GET /api/airports/search/?q=bogota`
- `GET /api/airports/BOG/`

Itinerary Service:

- `GET /api/itineraries/` — listar todos los itinerarios (HU-C1)
- `GET /api/itineraries/{itinerary_id}/` — consultar uno por ID (HU-C2)
- `PATCH /api/itineraries/{itinerary_id}/` — actualizar campos permitidos (HU-B5; bloqueado si COMPLETED → 409)
- `DELETE /api/itineraries/{itinerary_id}/` — eliminar itinerario (HU-C4, 204 sin body)
- `PATCH /api/itineraries/{itinerary_id}/status/` — cambiar estado (HU-C3)
- `POST /api/itineraries/` — crear itinerario
- `GET /api/itineraries/list/` — alias del listado (compatibilidad)

Ejemplo de respuesta del listado (200):

```json
[
  {
    "itinerary_id": "ITI-001",
    "origin_airport_id": "BOG",
    "destination_airport_id": "MDE",
    "start_date": "2026-04-20",
    "end_date": "2026-04-20",
    "start_time": "08:30:00",
    "end_time": "10:00:00",
    "status": "PENDING",
    "value": 350000.0
  }
]
```

Cambio de estado (PATCH, body) — **calculado automáticamente** según fecha y horario (zona `America/Bogota`):

| Condición | Estado |
|-----------|--------|
| Antes de la hora de inicio | `PENDING` (Pendiente) |
| Entre inicio y fin (inclusive) | `IN_PROGRESS` (En curso) |
| Después de la hora de fin | `COMPLETED` (Completado) |

El endpoint `PATCH /api/itineraries/{id}/status/` recalcula y devuelve el estado actual; no admite cambio manual.

Valores API: `PENDING`, `IN_PROGRESS`, `COMPLETED`.

Ejemplo de body para editar itinerario (PATCH parcial, HU-B5):

```json
{
  "origin_airport_id": "BOG",
  "destination_airport_id": "CLO",
  "start_date": "2026-04-21",
  "end_date": "2026-04-21",
  "start_time": "09:00",
  "end_time": "11:30",
  "value": 420000
}
```

Solo se puede editar si el estado es `PENDING` o `IN_PROGRESS`. Desde `COMPLETED` responde **409**.

En el MVP de un solo día de viaje, `start_date` y `end_date` coinciden con la fecha almacenada (`travel_date` al crear).

Ejemplo de body para crear itinerario:

```json
{
  "itinerary_id": "ITI-001",
  "origin_airport_id": "BOG",
  "destination_airport_id": "MDE",
  "travel_date": "2026-04-20",
    "start_time": "08:30",
    "end_time": "10:00",
    "value": 350000
  }
```

`value` es obligatorio al crear: número mayor o igual a cero (precio del viaje en COP). La bitácora (`GET /api/itineraries/summary/`) expone `total_value` como suma de todos los valores.

Las horas pueden enviarse como `HH:MM` o `HH:MM:SS`. La hora final debe ser estrictamente mayor que la inicial. Al crear, el estado inicial es **Pendiente** (HU-B3). Respuesta exitosa (201):

```json
{
  "message": "Itinerario creado correctamente",
  "itinerary_id": "ITI-001",
  "status": "PENDING",
  "value": 350000.0
}
```

El Itinerary Service valida que los aeropuertos existan consultando el Airport Service, rechaza `end_time <= start_time` y rechaza itinerarios que se solapen en la misma fecha (mensaje: «El itinerario se solapa con otro existente»).

## Alcance

Este repositorio es base tecnica para implementar historias de usuario del backlog Jira sin agregar funcionalidades fuera de alcance.
