from datetime import datetime
from typing import Dict

class GDPRCompliance:
    def __init__(self):
        self.user_consents = {}
        self.data_retention_days = 30

    async def record_user_consent(self, user_id: str, consents: Dict[str, bool]):
        """Enregistre le consentement RGPD de l'utilisateur"""
        self.user_consents[user_id] = {
            "consents": consents,
            "timestamp": datetime.now(),
            "ip_address": self._get_anonymized_ip()
        }

    async def delete_user_data(self, user_id: str):
        """Supprime toutes les données d'un utilisateur (droit à l'oubli)"""
        # Suppression des données utilisateur
        # Suppression historique d'apprentissage
        # Suppression des préférences 