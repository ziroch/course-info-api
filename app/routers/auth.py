from __future__ import annotations

import sqlite3
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models import Token, User, UserCreate
from app.repositories import UserRepository
from app.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
    hash_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


def get_user_repository() -> UserRepository:
    return UserRepository()


@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> User:
    try:
        created_user = repository.create_user(
            user=user,
            hashed_password=hash_password(user.password),
        )
    except sqlite3.IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El nombre de usuario o correo electrónico ya existe",
        ) from error

    return User(
        id=created_user.id,
        username=created_user.username,
        fullName=created_user.fullName,
        email=created_user.email,
        disabled=created_user.disabled,
    )


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> Token:
    user = authenticate_user(
        repository=repository,
        username=form_data.username,
        password=form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=user.username,
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/me", response_model=User)
def get_authenticated_user(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> User:
    return current_user