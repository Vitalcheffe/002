from dataclasses import dataclass
from datetime import datetime
import asyncio
from typing import Dict, List

@dataclass
class UserMetrics:
    total_requests: int
    success_rate: float
    average_response_time: float
    last_activity: datetime

class MetricsService:
    def __init__(self):
        self.user_metrics: Dict[str, UserMetrics] = {}
        self.global_metrics: Dict[str, float] = {}
        
    async def track_request(
        self,
        user_id: str,
        endpoint: str,
        duration: float,
        success: bool
    ):
        """Enregistre les métriques d'une requête"""
        # Mise à jour des métriques utilisateur
        if user_id not in self.user_metrics:
            self.user_metrics[user_id] = UserMetrics(0, 0.0, 0.0, datetime.now())
        
        metrics = self.user_metrics[user_id]
        metrics.total_requests += 1
        metrics.average_response_time = (
            (metrics.average_response_time * (metrics.total_requests - 1) + duration)
            / metrics.total_requests
        )
        metrics.last_activity = datetime.now()
        
        # Mise à jour des métriques globales
        self._update_global_metrics(endpoint, duration, success) 