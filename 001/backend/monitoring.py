from prometheus_client import Counter, Histogram
import logging
import sentry_sdk
from typing import Callable
from functools import wraps
import time

class MonitoringService:
    def __init__(self, sentry_dsn: str):
        self.request_counter = Counter(
            'http_requests_total',
            'Total des requêtes HTTP',
            ['method', 'endpoint', 'status']
        )
        self.response_time = Histogram(
            'http_response_time_seconds',
            'Temps de réponse HTTP'
        )
        
        sentry_sdk.init(dsn=sentry_dsn)
        
        # Configuration du logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def monitor_endpoint(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    self.request_counter.labels(
                        method='POST',
                        endpoint=func.__name__,
                        status='success'
                    ).inc()
                    return result
                except Exception as e:
                    self.request_counter.labels(
                        method='POST',
                        endpoint=func.__name__,
                        status='error'
                    ).inc()
                    self.logger.error(f"Erreur endpoint {func.__name__}: {str(e)}")
                    raise
                finally:
                    self.response_time.observe(time.time() - start_time)
            return wrapper
        return decorator 