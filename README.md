# task-api

A task management REST API built with FastAPI, as a DevOps portfolio project. The application is intentionally small. The focus is on testing, containers, CI/CD, Kubernetes, infrastructure as code, and monitoring.

## What it does

- Create a task: POST /tasks
- List tasks: GET /tasks
- Delete a task: DELETE /tasks/{task_id}
- Health check: GET /health
- Metrics for Prometheus: GET /metrics

## Tools used

- Python 3.12 and FastAPI for the application
- pytest for automated tests
- Docker for packaging the application
- GitHub Actions for the CI pipeline (tests, then build)
- Kubernetes (kind) for deployment
- Terraform for infrastructure, validated and planned only
- Prometheus and Grafana for monitoring
- Locust for load testing

## Run it locally

git clone https://github.com/Andreasloannidis/PipelineTasks.git
cd PipelineTasks
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app

Then open http://127.0.0.1:8000/docs in your browser.

## Run the tests

pytest -q

## Run with Docker

docker build -t task-api .
docker run -p 8000:8000 task-api

## Project structure

- app/ the FastAPI application
- tests/ the automated tests
- k8s/ Kubernetes manifests
- terraform/ Terraform configuration
- monitoring/ Prometheus configuration
- load/ Locust load test
- Dockerfile the container build
