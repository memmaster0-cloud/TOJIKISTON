"""Tests for the ToDo API.

Run with:
    pytest --cov=app tests/
"""

import pytest

from app import create_app
from app.main import store


@pytest.fixture(autouse=True)
def reset_store():
    """Clear the in-memory store before every test so tests don't
    depend on execution order."""
    store._todos.clear()
    yield


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_list_empty(client):
    resp = client.get("/todos")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_todo(client):
    resp = client.post("/todos", json={"title": "Buy milk"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["title"] == "Buy milk"
    assert body["done"] is False
    assert body["id"] == 1


def test_create_todo_missing_title(client):
    resp = client.post("/todos", json={})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_create_todo_title_not_string(client):
    resp = client.post("/todos", json={"title": 123})
    assert resp.status_code == 400


def test_list_after_create(client):
    client.post("/todos", json={"title": "A"})
    client.post("/todos", json={"title": "B"})
    resp = client.get("/todos")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_get_todo(client):
    created = client.post("/todos", json={"title": "Read book"}).get_json()
    resp = client.get(f"/todos/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Read book"


def test_get_missing_todo(client):
    resp = client.get("/todos/999")
    assert resp.status_code == 404


def test_update_todo_title(client):
    created = client.post("/todos", json={"title": "Old"}).get_json()
    resp = client.put(f"/todos/{created['id']}", json={"title": "New"})
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "New"


def test_update_todo_done(client):
    created = client.post("/todos", json={"title": "Task"}).get_json()
    resp = client.put(f"/todos/{created['id']}", json={"done": True})
    assert resp.status_code == 200
    assert resp.get_json()["done"] is True


def test_update_todo_invalid_title_type(client):
    created = client.post("/todos", json={"title": "Task"}).get_json()
    resp = client.put(f"/todos/{created['id']}", json={"title": 42})
    assert resp.status_code == 400


def test_update_todo_invalid_done_type(client):
    created = client.post("/todos", json={"title": "Task"}).get_json()
    resp = client.put(f"/todos/{created['id']}", json={"done": "yes"})
    assert resp.status_code == 400


def test_update_missing_todo(client):
    resp = client.put("/todos/999", json={"title": "New"})
    assert resp.status_code == 404


def test_delete_todo(client):
    created = client.post("/todos", json={"title": "Temp"}).get_json()
    resp = client.delete(f"/todos/{created['id']}")
    assert resp.status_code == 204
    assert client.get(f"/todos/{created['id']}").status_code == 404


def test_delete_missing_todo(client):
    resp = client.delete("/todos/999")
    assert resp.status_code == 404
