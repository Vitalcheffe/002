from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from services import DeepSeekService
from database import Database
from cache import CacheManager
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Deep Study AI")

# Initialisation des services
db = Database()
cache = CacheManager()
ai_service = DeepSeekService()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_content(request: dict):
    try:
        # Vérification du cache
        cache_key = f"analysis_{hash(request['content'])}"
        cached_result = await cache.get(cache_key)
        if cached_result:
            return cached_result

        # Analyse avec DeepSeek
        result = await ai_service.analyze(
            content=request['content'],
            type=request['type']
        )

        # Mise en cache
        await cache.set(cache_key, result)
        return result

    except Exception as e:
        logger.error(f"Erreur d'analyse: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 