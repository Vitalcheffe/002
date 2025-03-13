from deepseek import DeepSeek
import jwt
from typing import Dict, Any
import logging
from functools import lru_cache

class DeepSeekService:
    def __init__(self, api_key: str):
        self.client = DeepSeek(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    @lru_cache(maxsize=100)
    async def generate_content(self, content: str, type: str) -> Dict[str, Any]:
        try:
            prompt_map = {
                "summary": "Crée un résumé structuré et concis du texte suivant",
                "quiz": "Génère un quiz avec 5 questions à choix multiples",
                "mindmap": "Crée une structure de carte mentale avec les concepts clés"
            }
            
            response = await self.client.generate(
                model="deepseek-chat-33b",
                prompt=f"{prompt_map[type]}: {content}",
                temperature=0.7,
                max_length=2000
            )
            return {"content": response.text, "type": type}
        except Exception as e:
            self.logger.error(f"Erreur DeepSeek: {str(e)}")
            raise

    async def generate_summary(self, content: str) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Crée un résumé structuré et concis."},
                    {"role": "user", "content": content}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return {"summary": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Erreur génération résumé: {str(e)}")
            raise

    async def generate_quiz(self, content: str) -> Dict[str, Any]:
        # Logique de génération de quiz
        pass 