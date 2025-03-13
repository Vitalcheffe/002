import psutil
import asyncio
from datadog import initialize, statsd
from typing import Dict, Any

class SystemMonitor:
    def __init__(self, datadog_api_key: str):
        initialize(api_key=datadog_api_key)
        self.metrics = {}

    async def monitor_system_resources(self):
        while True:
            metrics = {
                'cpu.usage': psutil.cpu_percent(),
                'memory.usage': psutil.virtual_memory().percent,
                'disk.usage': psutil.disk_usage('/').percent,
                'network.connections': len(psutil.net_connections())
            }
            
            for metric, value in metrics.items():
                statsd.gauge(f'deepstudy.{metric}', value)
            
            if self._should_alert(metrics):
                await self._send_alert(metrics)
            
            await asyncio.sleep(60)

    def _should_alert(self, metrics: Dict[str, float]) -> bool:
        return (metrics['cpu.usage'] > 90 or 
                metrics['memory.usage'] > 85 or 
                metrics['disk.usage'] > 90)

    async def _send_alert(self, metrics: Dict[str, float]):
        # Envoi d'alertes via email/Slack/etc.
        pass 