# Flujo de autenticación JWT

```mermaid
sequenceDiagram
    actor Usuario
    participant API as FastAPI
    participant DB as SQLite
    participant JWT as Servicio JWT
    participant Endpoint as Endpoint protegido

    Usuario->>API: POST /auth/login
    API->>DB: Buscar usuario
    DB-->>API: Usuario y contraseña cifrada
    API->>API: Verificar contraseña

    alt Credenciales válidas
        API->>JWT: Generar token
        JWT-->>API: Access Token
        API-->>Usuario: Token JWT

        Usuario->>Endpoint: Authorization: Bearer TOKEN
        Endpoint->>JWT: Validar firma y expiración
        JWT-->>Endpoint: Token válido
        Endpoint-->>Usuario: Respuesta autorizada
    else Credenciales inválidas
        API-->>Usuario: 401 Unauthorized
    end
```

## Etapas

1. El usuario se registra mediante `/auth/register`.
2. La contraseña se almacena utilizando un hash Argon2.
3. El usuario envía sus credenciales a `/auth/login`.
4. La API verifica las credenciales.
5. La API genera un token JWT con tiempo de expiración.
6. El usuario envía el token como Bearer Token.
7. La API valida la firma y expiración.
8. El endpoint protegido permite o rechaza el acceso.