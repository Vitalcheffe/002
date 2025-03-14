from typing import List, Dict
from datetime import datetime
import asyncio
from database import Database

class ContentManager:
    def __init__(self, db: Database):
        self.db = db

    async def save_analysis(
        self,
        user_id: str,
        content: str,
        analysis_type: str,
        result: Dict
    ) -> str:
        """Sauvegarde une analyse"""
        analysis = {
            "user_id": user_id,
            "content": content,
            "type": analysis_type,
            "result": result,
            "created_at": datetime.utcnow(),
            "metadata": {
                "content_length": len(content),
                "processing_time": result.get("processing_time"),
                "language": result.get("detected_language")
            }
        }
        
        return await self.db.analyses.insert_one(analysis)

    async def get_user_history(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """Récupère l'historique des analyses d'un utilisateur"""
        return await self.db.analyses.find(
            {"user_id": user_id},
            sort=[("created_at", -1)],
            limit=limit,
            skip=offset
        ).to_list(length=limit)

    async def delete_analysis(self, analysis_id: str, user_id: str) -> bool:
        """Supprime une analyse"""
        result = await self.db.analyses.delete_one({
            "_id": analysis_id,
            "user_id": user_id
        })
        return result.deleted_count > 0 