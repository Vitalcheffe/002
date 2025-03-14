import aiohttp
import json
from typing import Dict, Any
import os

class DeepSeekService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/v1"
        self.session = aiohttp.ClientSession()

    async def analyze(self, content: str, type: str) -> Dict[str, Any]:
        """Analyse le contenu avec DeepSeek"""
        try:
            prompt = self._create_prompt(content, type)
            async with self.session.post(
                f"{self.api_url}/analyze",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"prompt": prompt, "max_tokens": 1000}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return self._format_response(result, type)
                else:
                    raise Exception(f"Erreur DeepSeek: {await response.text()}")
        except Exception as e:
            raise Exception(f"Erreur service IA: {str(e)}")

    def _create_prompt(self, content: str, type: str) -> str:
        prompts = {
            "summary": f"Résume ce texte de manière concise et structurée: {content}",
            "quiz": f"Crée un quiz de 5 questions basé sur ce contenu: {content}",
            "mindmap": f"Génère une structure de carte mentale pour: {content}"
        }
        return prompts.get(type, "")

    def _format_response(self, result: Dict, type: str) -> Dict:
        if type == "summary":
            return {"summary": result["text"]}
        elif type == "quiz":
            return {"questions": self._parse_quiz(result["text"])}
        elif type == "mindmap":
            return {"nodes": self._parse_mindmap(result["text"])}
        return result 