import threading

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

# Create the FastAPI application instance for pipelinetasks.
app = FastAPI()

# Counts every HTTP request, labelled by method and response status
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "status"])


@app.middleware("http")
async def count_requests(request, call_next):
    # Runs for every request: let the request through, then count it
    response = await call_next(request)
    # Do not count the /metrics scrapes themselves, only the task traffic
    if request.url.path != "/metrics":
        REQUEST_COUNT.labels(method=request.method, status=str(response.status_code)).inc()
    return response

# In-memory store keyed by the server-assigned task id.
tasks: dict[int, "Task"] = {}
_next_id = 1
# Sync routes run in a thread pool, so id assignment must be locked.
_store_lock = threading.Lock()


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
    with _store_lock:
        task = Task(id=_next_id, title=payload.title, done=False)
        tasks[_next_id] = task
        _next_id += 1
        return task


@app.get("/tasks")
def list_tasks() -> list[Task]:
    # Return every stored task; the list is empty when none exist.
    with _store_lock:
        return list(tasks.values())


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> Response:
    # Remove the task if it exists; otherwise return 404.
    with _store_lock:
        if task_id not in tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        del tasks[task_id]
    return Response(status_code=204)



@app.get("/metrics")
def metrics():
    # Returns the metrics in the plain-text format that Prometheus reads
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)