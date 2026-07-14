from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.models import TokenData, User, UserInDB
from app.repositories import UserRepository


SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "cambiar-esta-clave-secreta-antes-de-produccion-123456789",
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def authenticate_user(
    repository: UserRepository,
    username: str,
    password: str,
) -> UserInDB | None:
    user = repository.find_by_username(username)

    if user is None:
        return None

    if not verify_password(password, user.hashedPassword):
        return None

    return user


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    expiration = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": subject,
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError as error:
        raise credentials_exception from error

    user = repository.find_by_username(token_data.username)

    if user is None:
        raise credentials_exception

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario se encuentra deshabilitado",
        )

    return User(
        id=user.id,
        username=user.username,
        fullName=user.fullName,
        email=user.email,
        disabled=user.disabled,
    )