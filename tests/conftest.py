import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app


@pytest.fixture(autouse=True)
def clear_task_store() -> None:
    # Reset the in-memory store so each test starts from an empty list of tasks.
    main.tasks.clear()
    main._next_id = 1


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
