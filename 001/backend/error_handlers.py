from fastapi import Request, status
from fastapi.responses import JSONResponse
import sentry_sdk

async def deepseek_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Service IA temporairement indisponible",
            "details": str(exc)
        }
    )

async def database_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Erreur de base de données",
            "details": str(exc)
        }
    ) 