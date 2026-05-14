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

- `POST /api/itineraries/`
- `GET /api/itineraries/list/`

Ejemplo de body para crear itinerario:

```json
{
  "itinerary_id": "ITI-001",
  "origin_airport_id": "BOG",
  "destination_airport_id": "MDE",
  "travel_date": "2026-04-20",
  "start_time": "08:30",
  "end_time": "10:00"
}
```

Las horas pueden enviarse como `HH:MM` o `HH:MM:SS`. La hora final debe ser estrictamente mayor que la inicial. Al crear, el estado inicial es **Pendiente** (HU-B3). Respuesta exitosa (201):

```json
{
  "message": "Itinerario creado correctamente",
  "itinerary_id": "ITI-001",
  "status": "Pendiente"
}
```

El Itinerary Service valida que los aeropuertos existan consultando el Airport Service, rechaza `end_time <= start_time` y rechaza itinerarios que se solapen en la misma fecha (mensaje: «El itinerario se solapa con otro existente»). El listado (`GET .../list/`) incluye el campo `status`.

## Alcance

Este repositorio es base tecnica para implementar historias de usuario del backlog Jira sin agregar funcionalidades fuera de alcance.
