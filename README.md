# Course Info API

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)
![Pytest](https://img.shields.io/badge/Tests-Passing-success)
![Academic](https://img.shields.io/badge/Project-Academic-lightgrey)

API REST desarrollada con **FastAPI**, **SQLite**, **OpenAPI** y autenticación mediante **JWT**, orientada a la gestión de cursos, autores y calificaciones.

Este proyecto fue desarrollado como trabajo académico para la materia **Integración de Sistemas** de la Universidad UCOM.

---

## Índice

- [Descripción](#descripción)
- [Objetivos](#objetivos)
- [Funcionalidades](#funcionalidades)
- [Arquitectura](#arquitectura)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración JWT](#configuración-jwt)
- [Ejecución](#ejecución)
- [Documentación OpenAPI](#documentación-openapi)
- [Autenticación](#autenticación)
- [Endpoints](#endpoints)
- [Pruebas automáticas](#pruebas-automáticas)
- [Evidencias](#evidencias)
- [Documentación adicional](#documentación-adicional)
- [Autor](#autor)

---

## Descripción

Course Info API permite administrar información relacionada con:

- Cursos.
- Autores.
- Calificaciones.
- Usuarios autenticados.

La aplicación utiliza una arquitectura separada por responsabilidades:

- Routers para exponer endpoints.
- Modelos Pydantic para validación.
- Repositories para acceso a datos.
- SQLite como base de datos.
- JWT para autenticación y autorización.

---

## Objetivos

El proyecto tiene como objetivos:

- Aplicar los principios de diseño de APIs RESTful.
- Desarrollar servicios web con FastAPI.
- Documentar la API mediante OpenAPI y Swagger.
- Implementar autenticación basada en JWT.
- Proteger endpoints utilizando OAuth2 Password Flow.
- Extender la arquitectura existente con un CRUD completo de Grades.
- Implementar pruebas automáticas con Pytest.
- Utilizar Git y GitHub para control de versiones.

---

## Funcionalidades

### Courses

- Listar cursos.
- Consultar un curso por ID.
- Crear cursos.
- Actualizar cursos.
- Eliminar cursos.
- Agregar notas a un curso.

### Authors

- Listar autores.
- Consultar un autor mediante su handle.

### Grades

- Crear calificaciones.
- Listar calificaciones.
- Consultar una calificación por ID.
- Actualizar calificaciones.
- Eliminar calificaciones.
- Validar valores entre 1 y 100.

### Authentication

- Registrar usuarios.
- Cifrar contraseñas con Argon2.
- Iniciar sesión.
- Generar tokens JWT.
- Validar tokens.
- Controlar expiración.
- Consultar el usuario autenticado.
- Proteger endpoints de Courses, Authors y Grades.

---

## Arquitectura

La arquitectura detallada se encuentra en:

[Ver documentación de arquitectura](docs/ARCHITECTURE.md)

Resumen:

```mermaid
flowchart TD
    Client[Cliente / Swagger / Postman]
    API[FastAPI]
    Auth[Authentication Router]
    Courses[Courses Router]
    Authors[Authors Router]
    Grades[Grades Router]
    Security[JWT Security]
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

    Auth --> Repositories
    Courses --> Repositories
    Authors --> Repositories
    Grades --> Repositories

    Repositories --> Database
```

---

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| FastAPI | Framework web |
| Uvicorn | Servidor ASGI |
| SQLite | Base de datos |
| Pydantic | Validación de datos |
| PyJWT | Generación y validación de tokens |
| pwdlib / Argon2 | Hash de contraseñas |
| OAuth2 | Flujo de autenticación |
| Swagger UI | Documentación interactiva |
| ReDoc | Documentación alternativa |
| Pytest | Pruebas automáticas |
| Git | Control de versiones |
| GitHub | Repositorio remoto |

---

## Estructura del proyecto

```text
ucom-course-info-api/
│
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── authors.py
│   │   ├── courses.py
│   │   └── grades.py
│   │
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── repositories.py
│   └── security.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_authors.py
│   ├── test_courses.py
│   ├── test_database.py
│   └── test_grades.py
│
├── capturas/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── JWT_FLOW.md
│   └── openapi.json
│
├── CHANGELOG.md
├── LICENSE
├── README.md
├── db_init.sql
├── pyproject.toml
├── requirements.txt
└── IMPLEMENTATION_PLAN.md
```

---

## Instalación

### 1. Clonar el repositorio

```powershell
git clone https://github.com/ziroch/course-info-api.git
```

### 2. Ingresar en el proyecto

```powershell
cd course-info-api
```

### 3. Crear el entorno virtual

```powershell
python -m venv venv
```

### 4. Activar el entorno virtual

En Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Instalar dependencias

```powershell
pip install -r requirements.txt
```

---

## Configuración JWT

La aplicación utiliza una clave secreta para firmar los tokens JWT.

En PowerShell:

```powershell
$env:JWT_SECRET_KEY="una-clave-secreta-segura"
```

Para fines de desarrollo, el proyecto incluye una clave predeterminada.

No se recomienda utilizar esa clave en producción.

---

## Ejecución

Iniciar el servidor:

```powershell
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

---

## Documentación OpenAPI

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Esquema OpenAPI:

```text
http://127.0.0.1:8000/openapi.json
```

También se incluye una copia exportada en:

```text
docs/openapi.json
```

---

## Autenticación

### Registro

Endpoint:

```http
POST /auth/register
```

Ejemplo:

```json
{
  "username": "vjmartinez",
  "fullName": "Victor Martinez",
  "email": "vjmartinez@example.com",
  "password": "ClaveSegura123"
}
```

### Login

Endpoint:

```http
POST /auth/login
```

Datos enviados como formulario:

```text
username: vjmartinez
password: ClaveSegura123
```

Respuesta:

```json
{
  "access_token": "token_jwt_generado",
  "token_type": "bearer"
}
```

### Uso en Swagger

1. Abrir `/docs`.
2. Presionar **Authorize**.
3. Ingresar usuario y contraseña.
4. Confirmar la autorización.
5. Ejecutar los endpoints protegidos.

Swagger enviará automáticamente:

```http
Authorization: Bearer TOKEN
```

El flujo completo se documenta en:

[Ver flujo JWT](docs/JWT_FLOW.md)

---

## Endpoints

### Authentication

| Método | Endpoint | Descripción | JWT |
|---|---|---|---|
| POST | `/auth/register` | Registrar usuario | No |
| POST | `/auth/login` | Iniciar sesión | No |
| GET | `/auth/me` | Consultar usuario autenticado | Sí |

### Courses

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/courses` | Listar cursos |
| GET | `/courses/{course_id}` | Consultar curso |
| POST | `/courses` | Crear curso |
| PUT | `/courses/{course_id}` | Actualizar curso |
| DELETE | `/courses/{course_id}` | Eliminar curso |
| POST | `/courses/{course_id}/notes` | Agregar notas |

Todos requieren JWT.

### Authors

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/authors` | Listar autores |
| GET | `/authors/{handle}` | Consultar autor |

Todos requieren JWT.

### Grades

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/grades` | Listar calificaciones |
| GET | `/grades/{grade_id}` | Consultar calificación |
| POST | `/grades` | Crear calificación |
| PUT | `/grades/{grade_id}` | Actualizar calificación |
| DELETE | `/grades/{grade_id}` | Eliminar calificación |

Todos requieren JWT.

---

## Ejemplo de Grade

```json
{
  "authorId": 1,
  "courseId": "curso-python",
  "grade": 95
}
```

Respuesta:

```json
{
  "id": 1,
  "authorId": 1,
  "courseId": "curso-python",
  "grade": 95
}
```

---

## Códigos de respuesta

| Código | Descripción |
|---|---|
| 200 | Solicitud procesada correctamente |
| 201 | Recurso creado |
| 204 | Operación completada sin contenido |
| 401 | No autenticado o token inválido |
| 403 | Usuario deshabilitado |
| 404 | Recurso no encontrado |
| 409 | Usuario o email duplicado |
| 422 | Datos inválidos |

---

## Pruebas automáticas

Ejecutar:

```powershell
pytest
```

o:

```powershell
python -m pytest
```

Las pruebas cubren:

- Courses.
- Authors.
- Grades.
- Base de datos.
- Registro de usuarios.
- Inicio de sesión.
- Validación de contraseñas.
- Generación de JWT.
- Acceso autorizado.
- Acceso no autorizado.
- Tokens inválidos.

Resultado obtenido:

```text
35 passed, 1 warning
```

---

## Evidencias

### Swagger general

![Swagger general](capturas/01-swagger-general.png)
![Swagger general](capturas/01-swagger-general-2.png)
![Swagger general](capturas/01-swagger-general-3.png)


### Registro de usuario

![Registro](capturas/02-registro-usuario.png)
![Registro](capturas/02-registro-usuario-2.png)


### Login JWT

![Login JWT](capturas/03-login-jwt.png)
![Login JWT](capturas/03-login-jwt-2.png)

### Autorización OAuth2

![Authorize](capturas/04-authorize.png)
![Authorize](capturas/04-authorize-2.png)

### Acceso sin token

![Sin token](capturas/05-acceso-sin-token.png)

### Acceso con token

![Con token](capturas/06-acceso-con-token.png)

### Crear Grade

![Crear Grade](capturas/07-create-grade.png)

### Listar Grades

![Listar Grades](capturas/08-get-grades.png)

### Actualizar Grade

![Actualizar Grade](capturas/09-update-grade.png)
![Actualizar Grade](capturas/09-update-grade-2.png)

### Eliminar Grade

![Eliminar Grade](capturas/10-delete-grade.png)

### Pruebas Pytest

![Pytest](capturas/11-pytest.png)

### Repositorio GitHub

![GitHub](capturas/12-github-repositorio.png)

---

## Documentación adicional

- [Arquitectura](docs/ARCHITECTURE.md)
- [Flujo JWT](docs/JWT_FLOW.md)
- [Esquema OpenAPI](docs/openapi.json)
- [Historial de cambios](CHANGELOG.md)
- [Licencia](LICENSE)

---

## Autor

**Victor Martinez**

Universidad UCOM  
Materia: Integración de Sistemas  
Año: 2026

---

## Estado del proyecto

Proyecto académico finalizado y funcional.

- CRUD de Grades completado.
- JWT integrado.
- Swagger operativo.
- Endpoints protegidos.
- Pruebas automáticas aprobadas.
- Documentación disponible.
