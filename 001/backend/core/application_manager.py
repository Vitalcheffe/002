from typing import Optional
import asyncio
import logging
from datetime import datetime

class ApplicationManager:
    def __init__(self):
        self.startup_time = datetime.now()
        self.logger = logging.getLogger(__name__)
        self.is_healthy = True
        self.services = {}

    async def initialize(self):
        """Initialise tous les services de l'application"""
        try:
            # Initialisation des services critiques
            await self._init_database()
            await self._init_cache()
            await self._init_ai_service()
            await self._init_monitoring()
            
            # Démarrage des workers
            asyncio.create_task(self._run_background_tasks())
            
            self.logger.info("Application initialisée avec succès")
        except Exception as e:
            self.logger.critical(f"Erreur d'initialisation: {str(e)}")
            raise

    async def shutdown(self):
        """Arrêt gracieux de l'application"""
        self.logger.info("Début de l'arrêt de l'application")
        
        # Arrêt des services dans l'ordre
        await self._stop_background_tasks()
        await self._close_ai_service()
        await self._close_cache()
        await self._close_database()
        
        self.logger.info("Application arrêtée avec succès") 