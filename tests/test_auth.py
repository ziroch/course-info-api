from __future__ import annotations

from fastapi.testclient import TestClient


USER_DATA = {
    "username": "hernan",
    "fullName": "Hernan Silgueira",
    "email": "hernan@example.com",
    "password": "ClaveSegura123",
}


def register_user(client: TestClient) -> dict:
    response = client.post(
        "/auth/register",
        json=USER_DATA,
    )

    assert response.status_code == 201
    return response.json()


def login_user(client: TestClient) -> dict:
    response = client.post(
        "/auth/login",
        data={
            "username": USER_DATA["username"],
            "password": USER_DATA["password"],
        },
    )

    assert response.status_code == 200
    return response.json()


def test_register_user(
    auth_client: TestClient,
) -> None:
    data = register_user(auth_client)

    assert data["id"] is not None
    assert data["username"] == "hernan"
    assert data["fullName"] == "Hernan Silgueira"
    assert data["email"] == "hernan@example.com"
    assert data["disabled"] is False
    assert "password" not in data
    assert "hashedPassword" not in data


def test_duplicate_username_is_rejected(
    auth_client: TestClient,
) -> None:
    register_user(auth_client)

    response = auth_client.post(
        "/auth/register",
        json={
            "username": "hernan",
            "fullName": "Otro Usuario",
            "email": "otro@example.com",
            "password": "OtraClave123",
        },
    )

    assert response.status_code == 409


def test_duplicate_email_is_rejected(
    auth_client: TestClient,
) -> None:
    register_user(auth_client)

    response = auth_client.post(
        "/auth/register",
        json={
            "username": "otro_usuario",
            "fullName": "Otro Usuario",
            "email": "hernan@example.com",
            "password": "OtraClave123",
        },
    )

    assert response.status_code == 409


def test_short_password_is_rejected(
    auth_client: TestClient,
) -> None:
    response = auth_client.post(
        "/auth/register",
        json={
            "username": "usuario",
            "fullName": "Usuario Prueba",
            "email": "usuario@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422


def test_login_returns_access_token(
    auth_client: TestClient,
) -> None:
    register_user(auth_client)

    data = login_user(auth_client)

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password_is_rejected(
    auth_client: TestClient,
) -> None:
    register_user(auth_client)

    response = auth_client.post(
        "/auth/login",
        data={
            "username": "hernan",
            "password": "ClaveIncorrecta123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Usuario o contraseña incorrectos"
    )


def test_login_with_unknown_user_is_rejected(
    auth_client: TestClient,
) -> None:
    response = auth_client.post(
        "/auth/login",
        data={
            "username": "usuario_inexistente",
            "password": "ClaveSegura123",
        },
    )

    assert response.status_code == 401


def test_protected_endpoint_without_token_returns_401(
    auth_client: TestClient,
) -> None:
    response = auth_client.get("/grades")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_invalid_token_is_rejected(
    auth_client: TestClient,
) -> None:
    response = auth_client.get(
        "/grades",
        headers={
            "Authorization": "Bearer token-invalido",
        },
    )

    assert response.status_code == 401


def test_access_protected_endpoint_with_valid_token(
    auth_client: TestClient,
) -> None:
    register_user(auth_client)
    login_data = login_user(auth_client)

    token = login_data["access_token"]

    response = auth_client.get(
        "/grades",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200


def test_get_authenticated_user(
    auth_client: TestClient,
) -> None:
    register_user(auth_client)
    login_data = login_user(auth_client)

    token = login_data["access_token"]

    response = auth_client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "hernan"
    assert data["fullName"] == "Hernan Silgueira"
    assert data["email"] == "hernan@example.com"
    assert data["disabled"] is False