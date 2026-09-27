"""Core routes and in-memory storage for the ToDo API.

Endpoints
---------
GET    /health          -> liveness check
GET    /todos           -> list all todos
POST   /todos           -> create a todo, body: {"title": str}
GET    /todos/<id>      -> fetch one todo
PUT    /todos/<id>      -> update a todo, body: {"title"?: str, "done"?: bool}
DELETE /todos/<id>      -> delete a todo
"""

from __future__ import annotations

from itertools import count
from typing import Any

from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)


class TodoStore:
    """A tiny in-memory ToDo storage.

    Kept as a class (rather than bare module globals) so tests can
    create an isolated store per test if ever needed, and so the
    counter/state don't leak between instances.
    """

    def __init__(self) -> None:
        self._todos: dict[int, dict[str, Any]] = {}
        self._id_counter = count(1)

    def list_all(self) -> list[dict[str, Any]]:
        return list(self._todos.values())

    def create(self, title: str) -> dict[str, Any]:
        todo_id = next(self._id_counter)
        todo = {"id": todo_id, "title": title, "done": False}
        self._todos[todo_id] = todo
        return todo

    def get(self, todo_id: int) -> dict[str, Any] | None:
        return self._todos.get(todo_id)

    def update(self, todo_id: int, **fields: Any) -> dict[str, Any] | None:
        todo = self._todos.get(todo_id)
        if todo is None:
            return None
        todo.update({k: v for k, v in fields.items() if v is not None})
        return todo

    def delete(self, todo_id: int) -> bool:
        return self._todos.pop(todo_id, None) is not None


# Module-level store used by the blueprint. A fresh Flask app created via
# create_app() still shares this store; tests call `store.reset()` in a
# fixture to guarantee isolation between test cases.
store = TodoStore()


@api.get("/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@api.get("/todos")
def list_todos() -> tuple[list[dict[str, Any]], int]:
    return jsonify(store.list_all()), 200


@api.post("/todos")
def create_todo():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")
    if not title or not isinstance(title, str):
        return jsonify({"error": "'title' is required and must be a string"}), 400
    todo = store.create(title)
    return jsonify(todo), 201


@api.get("/todos/<int:todo_id>")
def get_todo(todo_id: int):
    todo = store.get(todo_id)
    if todo is None:
        return jsonify({"error": "todo not found"}), 404
    return jsonify(todo), 200


@api.put("/todos/<int:todo_id>")
def update_todo(todo_id: int):
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")
    done = payload.get("done")

    if title is not None and not isinstance(title, str):
        return jsonify({"error": "'title' must be a string"}), 400
    if done is not None and not isinstance(done, bool):
        return jsonify({"error": "'done' must be a boolean"}), 400

    todo = store.update(todo_id, title=title, done=done)
    if todo is None:
        return jsonify({"error": "todo not found"}), 404
    return jsonify(todo), 200


@api.delete("/todos/<int:todo_id>")
def delete_todo(todo_id: int):
    if not store.delete(todo_id):
        return jsonify({"error": "todo not found"}), 404
    return "", 204
