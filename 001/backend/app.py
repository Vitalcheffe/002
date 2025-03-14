from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from models import User, ContentRequest
from services import AIService
from database import get_db
from config import Settings
from fastapi.openapi.utils import get_openapi
from core.application_manager import ApplicationManager
from core.error_handler import ErrorHandler
from analytics.metrics_service import MetricsService
import time

app = FastAPI(title="Deep Study AI")
app_manager = ApplicationManager()
error_handler = ErrorHandler()
metrics_service = MetricsService()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Deep Study AI API",
        version="1.0.0",
        description="API pour la génération de contenus éducatifs avec DeepSeek",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.on_event("startup")
async def startup():
    await app_manager.initialize()

@app.on_event("shutdown")
async def shutdown():
    await app_manager.shutdown()

@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    await metrics_service.track_request(
        user_id=request.state.user_id,
        endpoint=request.url.path,
        duration=duration,
        success=response.status_code < 400
    )
    
    return response

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return await error_handler.handle_error(request, exc)

@app.post("/analyze")
async def analyze_content(request: ContentRequest):
    # Logique d'analyse du contenu
    pass

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 