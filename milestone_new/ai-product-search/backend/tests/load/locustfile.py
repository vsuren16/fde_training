from locust import HttpUser, task, between


class RecommendationUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def recommend(self):
        self.client.post("/products/recommend", json={"prompt": "suggest temple outfit"})

    @task(1)
    def list_products(self):
        self.client.get("/products")
