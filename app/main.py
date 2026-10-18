from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

# Create the FastAPI application instance for pipelinetasks.
app = FastAPI()

# In-memory store keyed by the server-assigned task id.
tasks: dict[int, "Task"] = {}
_next_id = 1


class TaskCreate(BaseModel):
    # Title is required and must stay within 1–100 characters.
    title: str = Field(..., min_length=1, max_length=100)


class Task(BaseModel):
    # The server assigns this integer id; clients never send it.
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    # New tasks start as not done.
    done: bool = False


@app.get("/health")
def health() -> dict[str, str]:
    # Simple liveness check used by local runs and later tests.
    return {"status": "ok"}


@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate) -> Task:
    # Assign the next integer id and keep the task in memory.
    global _next_id
    task = Task(id=_next_id, title=payload.title, done=False)
    tasks[_next_id] = task
    _next_id += 1
    return task


@app.get("/tasks")
def list_tasks() -> list[Task]:
    # Return every stored task; the list is empty when none exist.
    return list(tasks.values())


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> Response:
    # Remove the task if it exists; otherwise return 404.
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return Response(status_code=204)
