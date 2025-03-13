from typing import Optional, List
from datetime import datetime
import jwt
from passlib.hash import pbkdf2_sha256
from database import Database

class UserManager:
    def __init__(self, db: Database):
        self.db = db
        self.jwt_secret = os.getenv("JWT_SECRET")

    async def create_user(self, email: str, password: str, plan: str = "basic") -> Dict:
        """Création d'un nouvel utilisateur"""
        hashed_password = pbkdf2_sha256.hash(password)
        user = {
            "email": email,
            "password_hash": hashed_password,
            "plan": plan,
            "created_at": datetime.utcnow(),
            "last_login": None,
            "usage_stats": {
                "total_requests": 0,
                "last_request": None
            },
            "preferences": {
                "language": "fr",
                "notifications_enabled": True
            }
        }
        
        user_id = await self.db.users.insert_one(user)
        return self.generate_auth_tokens(str(user_id))

    async def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """Authentification utilisateur"""
        user = await self.db.users.find_one({"email": email})
        if user and pbkdf2_sha256.verify(password, user["password_hash"]):
            return self.generate_auth_tokens(str(user["_id"]))
        return None

    def generate_auth_tokens(self, user_id: str) -> Dict:
        """Génération des tokens JWT"""
        access_token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(hours=1)
            },
            self.jwt_secret,
            algorithm="HS256"
        )
        
        refresh_token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(days=30)
            },
            self.jwt_secret,
            algorithm="HS256"
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        } 