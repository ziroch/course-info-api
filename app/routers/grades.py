from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.models import Grade
from app.repositories import GradeRepository

from app.security import get_current_user


router = APIRouter(
    prefix="/grades",
    tags=["grades"],
    dependencies=[Depends(get_current_user)],
)


def get_grade_repository() -> GradeRepository:
    return GradeRepository()


@router.get("", response_model=list[Grade])
def get_grades(
    repository: Annotated[GradeRepository, Depends(get_grade_repository)],
) -> list[Grade]:
    return repository.get_all_grades()


@router.get("/{grade_id}", response_model=Grade)
def get_grade(
    grade_id: int,
    repository: Annotated[GradeRepository, Depends(get_grade_repository)],
) -> Grade:
    grade = repository.find_by_id(grade_id)

    if grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada",
        )

    return grade


@router.post("", response_model=Grade, status_code=status.HTTP_201_CREATED)
def create_grade(
    grade: Grade,
    repository: Annotated[GradeRepository, Depends(get_grade_repository)],
) -> Grade:
    new_grade = Grade(
        authorId=grade.authorId,
        courseId=grade.courseId,
        grade=grade.grade,
    )

    grade_id = repository.save_grade(new_grade)

    created_grade = repository.find_by_id(grade_id)

    if created_grade is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo crear la calificación",
        )

    return created_grade


@router.put("/{grade_id}", response_model=Grade)
def update_grade(
    grade_id: int,
    grade: Grade,
    repository: Annotated[GradeRepository, Depends(get_grade_repository)],
) -> Grade:
    existing_grade = repository.find_by_id(grade_id)

    if existing_grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada",
        )

    updated_grade = Grade(
        id=grade_id,
        authorId=grade.authorId,
        courseId=grade.courseId,
        grade=grade.grade,
    )

    repository.save_grade(updated_grade)
    return updated_grade


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: int,
    repository: Annotated[GradeRepository, Depends(get_grade_repository)],
) -> Response:
    existing_grade = repository.find_by_id(grade_id)

    if existing_grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada",
        )

    repository.delete_grade(grade_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)