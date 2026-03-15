from locust import HttpUser, task, between


class HealthUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def health(self):
        self.client.get("/health")
