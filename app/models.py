from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


def _filled(value: str) -> str:
    if value is None or not value.strip():
        raise ValueError("No value present!!")
    return value


class Course(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    length: int
    url: str
    notes: str | None = None

    @field_validator("id", "name", "url")
    @classmethod
    def required_text_must_be_filled(cls, value: str) -> str:
        return _filled(value)

    @field_validator("notes")
    @classmethod
    def optional_notes_must_be_filled(cls, value: str | None) -> str | None:
        if value is not None:
            return _filled(value)
        return value


class CourseUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str | None = None
    name: str
    length: int
    url: str
    notes: str | None = None

    @field_validator("id", "name", "url")
    @classmethod
    def text_must_be_filled(cls, value: str | None) -> str | None:
        if value is not None:
            return _filled(value)
        return value

    @field_validator("notes")
    @classmethod
    def optional_notes_must_be_filled(cls, value: str | None) -> str | None:
        if value is not None:
            return _filled(value)
        return value


class Author(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int | None = None
    firstName: str
    lastName: str
    handle: str

    @field_validator("firstName", "lastName", "handle")
    @classmethod
    def required_text_must_be_filled(cls, value: str) -> str:
        return _filled(value)


class Grade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int | None = None
    authorId: int
    courseId: str
    grade: int

    @field_validator("courseId")
    @classmethod
    def course_id_must_be_filled(cls, value: str) -> str:
        return _filled(value)

    @field_validator("grade")
    @classmethod
    def grade_must_be_valid(cls, value: int) -> int:
        if value < 1 or value > 100:
            raise ValueError("La calificación debe estar entre 1 y 100")
        return value


def course_from_row(row: Any) -> Course:
    return Course(
        id=row["id"],
        name=row["name"],
        length=row["length"],
        url=row["url"],
        notes=row["notes"],
    )


def author_from_row(row: Any) -> Author:
    return Author(
        id=row["id"],
        firstName=row["firstName"],
        lastName=row["lastName"],
        handle=row["handle"],
    )


def grade_from_row(row: Any) -> Grade:
    return Grade(
        id=row["id"],
        authorId=row["author_id"],
        courseId=row["course_id"],
        grade=row["grade"],
    )
class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    fullName: str
    email: str
    password: str

    @field_validator("username", "fullName", "email", "password")
    @classmethod
    def required_fields_must_be_filled(cls, value: str) -> str:
        return _filled(value)

    @field_validator("password")
    @classmethod
    def password_must_be_valid(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError(
                "La contraseña debe contener al menos 8 caracteres"
            )
        return value


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    username: str
    fullName: str
    email: str
    disabled: bool = False


class UserInDB(User):
    hashedPassword: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

def user_from_row(row: Any) -> UserInDB:
    return UserInDB(
        id=row["id"],
        username=row["username"],
        fullName=row["full_name"],
        email=row["email"],
        hashedPassword=row["hashed_password"],
        disabled=bool(row["disabled"]),
    )