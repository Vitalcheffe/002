from fastapi import Request, status
from fastapi.responses import JSONResponse
import sentry_sdk
import traceback

class ErrorHandler:
    def __init__(self):
        self.error_counts = {}
        
    async def handle_error(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        error_id = self._generate_error_id()
        
        # Log détaillé de l'erreur
        self._log_error(error_id, request, exc)
        
        # Notification si erreur critique
        if self._is_critical_error(exc):
            await self._notify_team(error_id, exc)
        
        # Réponse appropriée au client
        return self._create_error_response(error_id, exc)

    def _create_error_response(
        self,
        error_id: str,
        exc: Exception
    ) -> JSONResponse:
        if isinstance(exc, ValidationError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error_id": error_id,
                    "message": "Données invalides",
                    "details": str(exc)
                }
            )
        # Autres types d'erreurs...
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_id": error_id,
                "message": "Erreur interne du serveur"
            }
        ) 