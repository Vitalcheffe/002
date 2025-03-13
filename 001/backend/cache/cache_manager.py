from typing import Any, Optional
import redis
from functools import lru_cache
import json
import hashlib

class CacheManager:
    def __init__(self):
        self.redis = redis.Redis.from_url(os.getenv("REDIS_URL"))
        self.default_ttl = 3600  # 1 heure

    async def get_or_compute(
        self,
        key: str,
        compute_func,
        ttl: Optional[int] = None
    ) -> Any:
        """Récupère du cache ou calcule si absent"""
        cached = await self.get(key)
        if cached is not None:
            return cached

        result = await compute_func()
        await self.set(key, result, ttl or self.default_ttl)
        return result

    @lru_cache(maxsize=1000)
    async def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """Stocke une valeur dans le cache"""
        self.redis.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value)
        )

    async def invalidate_pattern(self, pattern: str) -> None:
        """Invalide toutes les clés correspondant au pattern"""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys) 