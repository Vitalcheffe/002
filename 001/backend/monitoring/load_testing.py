from locust import HttpUser, task, between
import asyncio
from prometheus_client import Counter, Histogram
import logging

class LoadTester:
    def __init__(self):
        self.response_times = Histogram(
            'api_response_seconds',
            'API response times',
            ['endpoint']
        )
        self.error_counter = Counter(
            'api_errors_total',
            'Total API errors',
            ['endpoint', 'error_type']
        )
        self.logger = logging.getLogger(__name__)

    async def run_load_test(self, endpoint: str, users: int, duration: int):
        """Exécute un test de charge sur un endpoint spécifique"""
        async def simulate_user(user_id: int):
            try:
                start_time = asyncio.get_event_loop().time()
                # Simulation de requête
                await asyncio.sleep(0.1)  # Simule le temps de réponse
                duration = asyncio.get_event_loop().time() - start_time
                self.response_times.labels(endpoint=endpoint).observe(duration)
            except Exception as e:
                self.error_counter.labels(
                    endpoint=endpoint,
                    error_type=type(e).__name__
                ).inc()
                self.logger.error(f"Erreur test de charge: {str(e)}")

        tasks = [simulate_user(i) for i in range(users)]
        await asyncio.gather(*tasks) 