from __future__ import annotations

from app.database import connect, init_database
from app.models import Grades
from app.repositories import GradesRepository


def test_database_initialization_creates_expected_tables(db_path: str) -> None:
    init_database(db_path)

    with connect(db_path) as connection:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

    assert {"courses", "authors", "calificacion"}.issubset(tables)


def test_calificacion_repository_persists_domain_model(db_path: str) -> None:
    repository = GradesRepository(db_path)

    repository.save_calificacion(Grades(authorId=1, courseId="course-1", nota=5))

    calificaciones = repository.get_all_calificaciones()
    assert len(calificaciones) == 1
    assert calificaciones[0].authorId == 1
    assert calificaciones[0].courseId == "course-1"
    assert calificaciones[0].nota == 5
