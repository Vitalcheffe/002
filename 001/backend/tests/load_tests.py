from locust import HttpUser, task, between

class DeepStudyAIUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def generate_summary(self):
        self.client.post("/analyze", json={
            "content": "Test content",
            "type": "summary"
        })

    @task(2)
    def generate_quiz(self):
        self.client.post("/analyze", json={
            "content": "Test content",
            "type": "quiz"
        }) 