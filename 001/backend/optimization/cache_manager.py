from functools import lru_cache
from typing import Any, Optional
import redis

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 heure

    @lru_cache(maxsize=1000)
    async def get_cached_response(self, key: str) -> Optional[Any]:
        return self.redis.get(key)

    async def cache_response(self, key: str, value: Any, ttl: int = None):
        self.redis.setex(key, ttl or self.default_ttl, value)

    async def invalidate_cache(self, pattern: str):
        """Invalide le cache basé sur un pattern"""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys) 