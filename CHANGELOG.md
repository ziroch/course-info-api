# Changelog

Todos los cambios importantes realizados en este proyecto se documentan en este archivo.

## [1.0.0] - 2026

### Agregado

- API REST desarrollada con FastAPI.
- Persistencia de datos mediante SQLite.
- Endpoints para la gestión de cursos.
- Endpoints para la consulta de autores.
- CRUD completo de calificaciones.
- Validación de calificaciones entre 1 y 100.
- Registro de usuarios.
- Almacenamiento seguro de contraseñas mediante Argon2.
- Inicio de sesión utilizando OAuth2 Password Flow.
- Generación de tokens JWT.
- Expiración y validación de tokens.
- Protección de endpoints de Courses, Authors y Grades.
- Endpoint para consultar el usuario autenticado.
- Documentación automática mediante Swagger UI.
- Documentación alternativa mediante ReDoc.
- Esquema OpenAPI exportado.
- Pruebas automáticas para Courses.
- Pruebas automáticas para Authors.
- Pruebas automáticas para Grades.
- Pruebas automáticas para autenticación JWT.
- Evidencias de funcionamiento.