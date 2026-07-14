# Course Info API

API REST desarrollada con **FastAPI** para la gestión de cursos, autores y calificaciones.  
El proyecto incorpora documentación automática mediante **OpenAPI/Swagger**, persistencia con **SQLite** y autenticación mediante **JSON Web Tokens (JWT)**.

## Objetivo

El proyecto fue desarrollado como parte de una actividad académica orientada a aplicar los siguientes conceptos:

- Diseño de APIs RESTful.
- Desarrollo de servicios web con FastAPI.
- Documentación automática con OpenAPI.
- Persistencia de datos mediante SQLite.
- Registro y autenticación de usuarios.
- Generación y validación de tokens JWT.
- Protección de endpoints.
- Pruebas automáticas con Pytest.

## Funcionalidades

### Courses

Permite gestionar cursos mediante operaciones REST:

- Listar cursos.
- Consultar un curso por ID.
- Crear cursos.
- Actualizar cursos.
- Eliminar cursos.
- Agregar notas a un curso.

### Authors

Permite:

- Listar autores.
- Consultar un autor mediante su identificador o handle.

### Grades

Se implementó un CRUD completo para las calificaciones:

- Crear una calificación.
- Listar todas las calificaciones.
- Consultar una calificación por ID.
- Actualizar una calificación.
- Eliminar una calificación.
- Validar que la calificación se encuentre entre 1 y 100.

### Autenticación JWT

La API incorpora:

- Registro de usuarios.
- Almacenamiento seguro de contraseñas mediante hash.
- Inicio de sesión con usuario y contraseña.
- Generación de tokens JWT.
- Tokens con tiempo de expiración.
- Protección de los endpoints de Courses, Authors y Grades.
- Consulta del usuario autenticado.

## Tecnologías utilizadas

- Python 3
- FastAPI
- Uvicorn
- SQLite
- Pydantic
- PyJWT
- pwdlib con Argon2
- OAuth2 Password Flow
- Pytest
- Swagger UI
- OpenAPI

## Estructura del proyecto

```text
course-info-python/
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
├── db_init.sql
├── requirements.txt
├── pyproject.toml
├── IMPLEMENTATION_PLAN.md
└── README.md