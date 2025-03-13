from prometheus_client import Counter, Histogram, Gauge
import psutil
import asyncio

class SystemMetrics:
    def __init__(self):
        self.cpu_usage = Gauge('cpu_usage_percent', 'CPU usage in percent')
        self.memory_usage = Gauge('memory_usage_percent', 'Memory usage in percent')
        self.api_latency = Histogram(
            'api_latency_seconds',
            'API endpoint latency',
            ['endpoint']
        )
        self.deepseek_errors = Counter(
            'deepseek_errors_total',
            'Total DeepSeek API errors'
        )
        
    async def collect_metrics(self):
        while True:
            self.cpu_usage.set(psutil.cpu_percent())
            self.memory_usage.set(psutil.virtual_memory().percent)
            await asyncio.sleep(15) 