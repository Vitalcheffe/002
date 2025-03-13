from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import asyncio

class AnalyticsService:
    def __init__(self, db: Database):
        self.db = db

    async def generate_user_report(self, user_id: str) -> Dict:
        """Génère un rapport d'utilisation pour un utilisateur"""
        analyses = await self.db.analyses.find(
            {"user_id": user_id}
        ).to_list(length=None)
        
        df = pd.DataFrame(analyses)
        
        return {
            "total_analyses": len(analyses),
            "analyses_by_type": df["type"].value_counts().to_dict(),
            "average_content_length": df["metadata.content_length"].mean(),
            "usage_over_time": self._generate_usage_graph(df),
            "most_active_hours": self._get_most_active_hours(df)
        }

    async def generate_system_report(self) -> Dict:
        """Génère un rapport système global"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_users": {"$sum": 1},
                    "total_analyses": {"$sum": "$usage_stats.total_requests"},
                    "average_response_time": {"$avg": "$metadata.processing_time"}
                }
            }
        ]
        
        stats = await self.db.users.aggregate(pipeline).to_list(length=1)
        return stats[0] if stats else {}

    def _generate_usage_graph(self, df: pd.DataFrame) -> Dict:
        """Génère un graphique d'utilisation"""
        df['date'] = pd.to_datetime(df['created_at'])
        usage_by_date = df.groupby('date').size()
        
        fig = px.line(
            usage_by_date,
            title='Utilisation au fil du temps'
        )
        return fig.to_dict() 