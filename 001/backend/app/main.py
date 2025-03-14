from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .services import AIService, PaymentService, UserService
from .database import get_db
from .auth import get_current_user
from .models import AnalysisRequest, User
from .config import Settings
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration app
app = FastAPI(title="Deep Study AI")
settings = Settings()

# Services
ai_service = AIService()
payment_service = PaymentService()
user_service = UserService()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_content(
    request: AnalysisRequest,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        # Vérification des limites d'utilisation
        if not await user_service.check_usage_limits(current_user.id):
            raise HTTPException(status_code=429, detail="Limite d'utilisation atteinte")

        # Analyse du contenu
        result = await ai_service.analyze(
            content=request.content,
            type=request.type,
            user=current_user
        )

        # Enregistrement de l'utilisation
        await user_service.record_usage(current_user.id, request.type)

        return result
    except Exception as e:
        logger.error(f"Erreur analyse: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/subscribe")
async def create_subscription(
    plan_id: str,
    current_user: User = Depends(get_current_user)
):
    try:
        subscription = await payment_service.create_subscription(
            user_id=current_user.id,
            plan_id=plan_id
        )
        return subscription
    except Exception as e:
        logger.error(f"Erreur abonnement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 