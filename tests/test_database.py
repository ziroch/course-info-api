from __future__ import annotations

from app.database import connect, init_database
from app.models import Grade
from app.repositories import GradeRepository


def test_database_initialization_creates_expected_tables(
    db_path: str,
) -> None:
    init_database(db_path)

    with connect(db_path) as connection:
        tables = {
            row["name"]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            ).fetchall()
        }

    assert {
        "courses",
        "authors",
        "grades",
        "users",
    }.issubset(tables)


def test_grade_repository_persists_domain_model(
    db_path: str,
) -> None:
    repository = GradeRepository(db_path)

    grade_id = repository.save_grade(
        Grade(
            authorId=1,
            courseId="course-1",
            grade=5,
        )
    )

    grades = repository.get_all_grades()

    assert grade_id is not None
    assert len(grades) == 1
    assert grades[0].id == grade_id
    assert grades[0].authorId == 1
    assert grades[0].courseId == "course-1"
    assert grades[0].grade == 5