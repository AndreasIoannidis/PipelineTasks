from fastapi.testclient import TestClient


# GET /health returns 200 with the body {"status": "ok"}.
def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# POST /tasks with a valid title returns 201 and the task has done set to false.
def test_create_task_with_valid_title(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["done"] is False
    assert isinstance(body["id"], int)


# POST /tasks without a title returns 422.
def test_create_task_without_title(client: TestClient) -> None:
    response = client.post("/tasks", json={})
    assert response.status_code == 422


# POST /tasks with an empty title returns 422.
def test_create_task_with_empty_title(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


# POST /tasks with a title of 101 characters returns 422.
def test_create_task_with_title_too_long(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "a" * 101})
    assert response.status_code == 422


# POST /tasks with a title of exactly 100 characters returns 201.
def test_create_task_with_title_of_max_length(client: TestClient) -> None:
    title = "a" * 100
    response = client.post("/tasks", json={"title": title})
    assert response.status_code == 201
    assert response.json()["title"] == title


# After creating a task, GET /tasks returns a list that contains it.
def test_list_tasks_contains_created_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Walk the dog"}).json()
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert created in tasks


# DELETE /tasks/{id} for an existing task returns 204, and the task no longer appears in GET /tasks.
def test_delete_existing_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Trash"}).json()
    delete_response = client.delete(f"/tasks/{created['id']}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""
    remaining = client.get("/tasks").json()
    assert created not in remaining


# DELETE /tasks/{id} for an id that does not exist returns 404.
def test_delete_missing_task(client: TestClient) -> None:
    response = client.delete("/tasks/999")
    assert response.status_code == 404
