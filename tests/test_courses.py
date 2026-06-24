from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_and_get_course(client: TestClient) -> None:
    response = client.post(
        "/courses/",
        json={"id": "123", "name": "ABC", "length": 40, "url": "//", "notes": None},
    )
    assert response.status_code == 204

    response = client.get("/courses/123")

    assert response.status_code == 200
    assert response.json() == {
        "id": "123",
        "name": "ABC",
        "length": 40,
        "url": "//",
        "notes": None,
    }


def test_courses_are_sorted_by_id(client: TestClient) -> None:
    client.post("/courses/", json={"id": "456", "name": "DEF", "length": 11, "url": "/A/"})
    client.post("/courses/", json={"id": "123", "name": "ABC", "length": 40, "url": "//"})

    response = client.get("/courses")

    assert response.status_code == 200
    assert [course["id"] for course in response.json()] == ["123", "456"]


def test_update_uses_path_id(client: TestClient) -> None:
    client.post("/courses/", json={"id": "123", "name": "ABC", "length": 40, "url": "//"})

    response = client.put(
        "/courses/123",
        json={"id": "456", "name": "DEF", "length": 11, "url": "/A/", "notes": "ABCe"},
    )
    assert response.status_code == 204

    response = client.get("/courses/123")

    assert response.status_code == 200
    assert response.json() == {
        "id": "123",
        "name": "DEF",
        "length": 11,
        "url": "/A/",
        "notes": "ABCe",
    }


def test_add_notes_consumes_plain_text(client: TestClient) -> None:
    client.post("/courses/", json={"id": "123", "name": "ABC", "length": 40, "url": "//"})

    response = client.post(
        "/courses/123/notes",
        content="Hello",
        headers={"content-type": "text/plain"},
    )
    assert response.status_code == 204

    response = client.get("/courses/123")
    assert response.json()["notes"] == "Hello"


def test_delete_existing_course(client: TestClient) -> None:
    client.post("/courses/", json={"id": "123", "name": "ABC", "length": 40, "url": "//"})

    response = client.delete("/courses/123")
    assert response.status_code == 204

    response = client.get("/courses/123")
    assert response.status_code == 404


def test_missing_course_returns_404(client: TestClient) -> None:
    assert client.get("/courses/missing").status_code == 404
    assert client.delete("/courses/missing").status_code == 404


def test_blank_required_course_field_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/courses/",
        json={"id": " ", "name": "ABC", "length": 40, "url": "//"},
    )

    assert response.status_code == 422


def test_blank_notes_are_rejected_when_present(client: TestClient) -> None:
    response = client.post(
        "/courses/",
        json={"id": "123", "name": "ABC", "length": 40, "url": "//", "notes": " "},
    )

    assert response.status_code == 422
