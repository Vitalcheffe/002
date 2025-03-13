from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Optional
import jwt
from cryptography.fernet import Fernet
import redis
from ratelimit import limits, RateLimitException

class SecurityService:
    def __init__(self, secret_key: str, redis_url: str):
        self.secret_key = secret_key
        self.fernet = Fernet(secret_key)
        self.redis_client = redis.from_url(redis_url)
        self.security = HTTPBearer()

    def encrypt_data(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    @limits(calls=100, period=60)  # 100 appels par minute
    async def rate_limit_check(self, user_id: str):
        key = f"rate_limit:{user_id}"
        if self.redis_client.get(key):
            raise RateLimitException("Trop de requêtes")
        self.redis_client.setex(key, 60, 1)

    def create_csrf_token(self, user_id: str) -> str:
        return jwt.encode(
            {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)},
            self.secret_key,
            algorithm="HS256"
        )

    def verify_csrf_token(self, token: str) -> bool:
        try:
            jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True
        except:
            return False 