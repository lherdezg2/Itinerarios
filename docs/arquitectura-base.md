# Arquitectura Base del MVP

## Decision principal

Se usa arquitectura hexagonal por microservicio para asegurar separacion de responsabilidades y facilitar trazabilidad academica.

## En Django

- Las views en `adapters/inbound/rest` solo traducen HTTP a llamadas de casos de uso.
- La logica de negocio se concentra en `application/use_cases` y `domain`.
- Los puertos (`application/ports`) definen contratos para no acoplar dominio a infraestructura.

## Estado actual

- Airport Service: busqueda y consulta simple en adapter de salida en memoria.
- Itinerary Service: creacion/listado simple con validaciones basicas y adapter de repositorio en memoria.
- Docker: dos Dockerfile + compose para orquestar servicios y DB.

Esto permite iniciar las HU del backlog de manera incremental, sin rehacer estructura.
