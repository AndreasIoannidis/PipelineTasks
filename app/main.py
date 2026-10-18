from fastapi import FastAPI

# Create the FastAPI application instance for pipelinetasks.
app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    # Simple liveness check used by local runs and later tests.
    return {"status": "ok"}
