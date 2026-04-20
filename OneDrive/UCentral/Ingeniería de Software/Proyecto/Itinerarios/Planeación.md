# Sistema de Planificación de Itinerarios de Viaje

Proyecto académico desarrollado para y desarrollo de microservicios.

---

## 📌 Contexto del Proyecto

El objetivo del proyecto es desarrollar un sistema básico de planificación de viajes que permita a los usuarios:

- Consultar aeropuertos colombianos
- Visualizar aeropuertos en un mapa interactivo
- Crear y gestionar itinerarios de viaje
- Validar que los aeropuertos utilizados existan realmente
- Registrar una bitácora básica de viajes

El proyecto se desarrolla como un **MVP académico**, priorizando:
- Claridad arquitectónica
- Correcta separación de responsabilidades
- Coherencia entre planeación, diseño y código

No se busca construir un producto completo ni abordar escenarios avanzados.

---

## 🧱 Arquitectura del Sistema

El sistema está basado en los siguientes principios:

- **Arquitectura de Microservicios**
- **Arquitectura Hexagonal (Ports & Adapters)**
- **Patrón Adapter**
- **Separación dominio / infraestructura**
- **Comunicación HTTP entre servicios**
- **Dockerización del entorno**

### Microservicios principales
- **Airport Service**
- **Itinerary Service**

Cada microservicio:
- Es independiente
- Implementa arquitectura hexagonal
- Tiene su propio Dockerfile
- No comparte base de datos con otros servicios

---

## 🧭 Arquitecturas y Diagramas

El diseño del sistema está soportado por los siguientes diagramas:

### Arquitectura de Negocio
- Diagrama BPMN (Bizagi Modeler)

### Arquitectura de Información
- Diagrama Entidad–Relación (ER)

### Arquitectura de Aplicaciones
- Diagrama de Componentes (UML)
- Diagramas de Arquitectura Hexagonal:
  - Airport Service
  - Itinerary Service
- Diagrama de Contenedores (C4 – Nivel 2)

### Arquitectura Tecnológica
- Diagrama de Despliegue (UML)

Todos los diagramas son coherentes entre sí y representan fielmente la arquitectura implementada en el código.

---

## 📋 Planeación del Proyecto (Backlog)

La planeación del proyecto se realizó inicialmente en **Jira** bajo un enfoque ágil.  
Debido a que se trataba de una versión de prueba, el backlog definitivo se documenta en este repositorio como referencia formal del desarrollo.

### Épicas del Proyecto

### A – Aeropuertos
- Consulta de aeropuertos por ID
- Búsqueda de aeropuertos por nombre o ciudad
- Visualización de aeropuertos en mapa
- Adaptación de API externa mediante Adapter
- Selección y validación de aeropuertos

### B – Itinerarios
- Creación de itinerarios de viaje
- Validación de aeropuertos
- Reglas de negocio (fechas, solapes, estados)
- Consulta de bitácora de viajes

### C – Acceso y Roles
- Inicio de sesión
- Rol Gestor (básico)

### D – Plataforma y Documentación
- Aplicación web básica
- Documentación automática (Swagger)
- Dockerización del sistema

### E – Integración
- Comunicación HTTP entre microservicios

---

## 🚀 Versiones del Proyecto

### Versión 1.0 – MVP
Incluye:
- Consulta de aeropuertos
- Visualización básica en mapa
- Creación básica de itinerarios
- Validación de aeropuertos
- Arquitectura hexagonal aplicada
- Docker
- Swagger

### Versión 1.1 – Extensiones (si se alcanza)
Incluye:
- Validación de solapes
- Estados del itinerario
- Bitácora de viajes
- Rol Gestor

El desarrollo se realiza **estrictamente por versiones**, sin implementar funcionalidades fuera del alcance definido.

---

## 🐳 Dockerización

El sistema está completamente dockerizado:

- Cada microservicio cuenta con su propio `Dockerfile`
- Existe un archivo `docker-compose.yml` para levantar:
  - Airport Service
  - Itinerary Service
  - Base de datos (si aplica)

No se incluye:
- Kubernetes
- Configuración productiva
- CI/CD avanzado

Docker se utiliza como mecanismo de estandarización y evidencia arquitectónica.

---

## 🧑‍💻 Stack Tecnológico

- **Lenguaje:** Python
- **Framework Backend:** Django
- **Arquitectura:** Hexagonal
- **Contenedores:** Docker
- **Gestión de código:** Git + GitHub
- **Asistencia de desarrollo:** GitHub Copilot
- **Diagramas:** draw.io, Bizagi Modeler

Django se utiliza de forma controlada:
- Las views no contienen lógica de negocio
- El dominio no depende de Django, ORM ni REST
- La arquitectura definida prima sobre el framework

---

## 🤖 Uso de GitHub Copilot

GitHub Copilot se utiliza como asistente de escritura de código, no como diseñador de arquitectura.

El desarrollo está guiado por un **prompt base**, el cual instruye a Copilot a:
- Respetar la arquitectura hexagonal
- Implementar solo historias del backlog
- No mezclar capas
- Priorizar claridad sobre complejidad

---

## ✅ Estado del Proyecto

- Planeación: ✅ Completada
- Diseño arquitectónico: ✅ Completado
- Auditoría de coherencia: ✅ Aprobada
- Implementación: 🚧 En desarrollo (MVP)

---

## 📚 Observación Final

Este proyecto prioriza la correcta aplicación de principios de ingeniería de software, la coherencia entre diseño y código, y la trazabilidad del proceso de desarrollo, por encima de la complejidad funcional.

---