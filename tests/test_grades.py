from __future__ import annotations

from fastapi.testclient import TestClient


def create_grade(
    client: TestClient,
    grade_value: int = 90,
) -> dict:
    response = client.post(
        "/grades",
        json={
            "authorId": 1,
            "courseId": "curso-python",
            "grade": grade_value,
        },
    )

    assert response.status_code == 201
    return response.json()


def test_create_grade(client: TestClient) -> None:
    data = create_grade(client)

    assert data["id"] is not None
    assert data["authorId"] == 1
    assert data["courseId"] == "curso-python"
    assert data["grade"] == 90


def test_get_all_grades(client: TestClient) -> None:
    create_grade(client, 90)
    create_grade(client, 75)

    response = client.get("/grades")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["grade"] == 90
    assert data[1]["grade"] == 75


def test_get_grade_by_id(client: TestClient) -> None:
    created_grade = create_grade(client)

    grade_id = created_grade["id"]

    response = client.get(f"/grades/{grade_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == grade_id
    assert data["authorId"] == 1
    assert data["courseId"] == "curso-python"
    assert data["grade"] == 90


def test_update_grade(client: TestClient) -> None:
    created_grade = create_grade(client, 80)

    grade_id = created_grade["id"]

    response = client.put(
        f"/grades/{grade_id}",
        json={
            "authorId": 1,
            "courseId": "curso-python",
            "grade": 95,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == grade_id
    assert data["grade"] == 95

    get_response = client.get(f"/grades/{grade_id}")

    assert get_response.status_code == 200
    assert get_response.json()["grade"] == 95


def test_delete_grade(client: TestClient) -> None:
    created_grade = create_grade(client)

    grade_id = created_grade["id"]

    response = client.delete(f"/grades/{grade_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/grades/{grade_id}")

    assert get_response.status_code == 404


def test_missing_grade_returns_404(
    client: TestClient,
) -> None:
    response = client.get("/grades/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Calificación no encontrada"
    )


def test_update_missing_grade_returns_404(
    client: TestClient,
) -> None:
    response = client.put(
        "/grades/9999",
        json={
            "authorId": 1,
            "courseId": "curso-python",
            "grade": 90,
        },
    )

    assert response.status_code == 404


def test_delete_missing_grade_returns_404(
    client: TestClient,
) -> None:
    response = client.delete("/grades/9999")

    assert response.status_code == 404


def test_grade_below_minimum_is_rejected(
    client: TestClient,
) -> None:
    response = client.post(
        "/grades",
        json={
            "authorId": 1,
            "courseId": "curso-python",
            "grade": 0,
        },
    )

    assert response.status_code == 422


def test_grade_above_maximum_is_rejected(
    client: TestClient,
) -> None:
    response = client.post(
        "/grades",
        json={
            "authorId": 1,
            "courseId": "curso-python",
            "grade": 101,
        },
    )

    assert response.status_code == 422