from pydantic_settings import BaseSettings
import ssl
import logging.config

class ProductionConfig(BaseSettings):
    # Paramètres de l'application
    APP_NAME: str = "Deep Study AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    
    # Sécurité
    SSL_CONTEXT = ssl.create_default_context()
    SSL_CONTEXT.minimum_version = ssl.TLSVersion.TLSv1_3
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # DeepSeek
    DEEPSEEK_TIMEOUT: int = 30
    DEEPSEEK_MAX_TOKENS: int = 2000
    
    # Cache
    REDIS_MAX_CONNECTIONS: int = 100
    CACHE_TTL: int = 3600
    
    # Base de données
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    class Config:
        env_file = ".env.production" 