from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
import json

class APIDocumentation:
    def __init__(self, app: FastAPI):
        self.app = app

    def generate_openapi_spec(self):
        """Génère la documentation OpenAPI"""
        return get_openapi(
            title="Deep Study AI API",
            version="1.0.0",
            description="API complète pour la plateforme Deep Study AI",
            routes=self.app.routes,
            tags=[
                {"name": "auth", "description": "Authentification"},
                {"name": "content", "description": "Gestion du contenu"},
                {"name": "ai", "description": "Services d'IA"}
            ]
        )

    def save_documentation(self, path: str = "docs/api-spec.json"):
        """Sauvegarde la documentation au format JSON"""
        with open(path, 'w') as f:
            json.dump(self.generate_openapi_spec(), f, indent=2) 