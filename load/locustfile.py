from locust import HttpUser, task, between
import random


class TaskUser(HttpUser):
    # Each simulated user waits 1 to 2 seconds between actions
    wait_time = between(1, 2)

    def on_start(self):
        # Remember the ids of tasks this user created, so it can delete them later
        self.created_ids = []

    @task(3)
    def create_task(self):
        # Creating tasks is the most common action (weight 3)
        response = self.client.post("/tasks", json={"title": f"load task {random.randint(1, 10000)}"})
        if response.status_code == 201:
            self.created_ids.append(response.json()["id"])

    @task(2)
    def list_tasks(self):
        # Listing tasks is the second most common action (weight 2)
        self.client.get("/tasks")

    @task(1)
    def delete_task(self):
        # Deleting is the least common action (weight 1)
        if self.created_ids:
            task_id = self.created_ids.pop()
            self.client.delete(f"/tasks/{task_id}", name="/tasks/[id]")