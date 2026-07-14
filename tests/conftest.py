from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.database import DATABASE_ENV_VAR, init_database
from app.main import app
from app.models import User
from app.security import get_current_user


def override_get_current_user() -> User:
    """
    Usuario autenticado simulado para probar los endpoints
    de Courses, Authors y Grades.
    """
    return User(
        id=1,
        username="testuser",
        fullName="Test User",
        email="test@example.com",
        disabled=False,
    )


@pytest.fixture()
def db_path(tmp_path) -> Iterator[str]:
    path = str(tmp_path / "courses.db")

    previous = os.environ.get(DATABASE_ENV_VAR)
    os.environ[DATABASE_ENV_VAR] = path

    init_database(path)

    try:
        yield path
    finally:
        if previous is None:
            os.environ.pop(DATABASE_ENV_VAR, None)
        else:
            os.environ[DATABASE_ENV_VAR] = previous


@pytest.fixture()
def client(db_path: str) -> Iterator[TestClient]:
    """
    Cliente con usuario autenticado simulado.
    """
    app.dependency_overrides[get_current_user] = (
        override_get_current_user
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def auth_client(db_path: str) -> Iterator[TestClient]:
    """
    Cliente sin autenticación simulada.

    Permite probar el funcionamiento real del registro,
    login y validación de tokens JWT.
    """
    app.dependency_overrides.clear()

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()