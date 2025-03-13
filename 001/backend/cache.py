from redis import Redis
from typing import Any, Optional
import json
import logging

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url)
        self.logger = logging.getLogger(__name__)

    async def set_cache(
        self, 
        key: str, 
        value: Any, 
        expire_time: int = 3600
    ):
        try:
            self.redis.setex(
                key,
                expire_time,
                json.dumps(value)
            )
        except Exception as e:
            self.logger.error(f"Erreur cache: {str(e)}")

    async def get_cache(self, key: str) -> Optional[Any]:
        try:
            data = self.redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            self.logger.error(f"Erreur lecture cache: {str(e)}")
            return None 