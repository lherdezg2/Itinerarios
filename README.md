# Itinerarios - MVP Academico

Proyecto base para Ingenieria de Software II con arquitectura de microservicios y arquitectura hexagonal.

## Estructura

- `airport-service`: microservicio de consulta de aeropuertos.
- `itinerary-service`: microservicio de gestion de itinerarios.
- `docker-compose.yml`: levanta ambos servicios y base de datos.

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
  "start_date": "2026-04-20",
  "end_date": "2026-04-23"
}
```

## Alcance

Este repositorio es base tecnica para implementar historias de usuario del backlog Jira sin agregar funcionalidades fuera de alcance.
