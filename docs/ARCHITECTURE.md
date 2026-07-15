# Arquitectura del proyecto

Course Info API utiliza una arquitectura organizada por responsabilidades.

```mermaid
flowchart TD
    Client[Cliente / Swagger UI / Postman]

    API[FastAPI Application]

    Auth[Router de autenticación]
    Courses[Router de Courses]
    Authors[Router de Authors]
    Grades[Router de Grades]

    Security[Seguridad JWT y OAuth2]
    Models[Modelos Pydantic]
    Repositories[Repositories]
    Database[(SQLite)]

    Client --> API

    API --> Auth
    API --> Courses
    API --> Authors
    API --> Grades

    Auth --> Security
    Courses --> Security
    Authors --> Security
    Grades --> Security

    Auth --> Models
    Courses --> Models
    Authors --> Models
    Grades --> Models

    Auth --> Repositories
    Courses --> Repositories
    Authors --> Repositories
    Grades --> Repositories

    Repositories --> Database
```

## Componentes

### FastAPI Application

La aplicación principal registra los routers, configura OpenAPI y administra el ciclo de vida de la base de datos.

### Routers

Los routers exponen los endpoints REST:

- Authentication
- Courses
- Authors
- Grades

### Models

Los modelos Pydantic validan los datos de entrada y salida.

### Repositories

Los repositories encapsulan las operaciones realizadas sobre SQLite.

### Security

El módulo de seguridad administra:

- Hash de contraseñas.
- Validación de credenciales.
- Creación de tokens JWT.
- Validación de tokens.
- Obtención del usuario autenticado.

### Database

SQLite almacena:

- Cursos.
- Autores.
- Calificaciones.
- Usuarios.