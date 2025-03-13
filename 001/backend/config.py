from pydantic_settings import BaseSettings

class ProductionSettings(BaseSettings):
    # DeepSeek
    DEEPSEEK_API_KEY: str
    DEEPSEEK_MODEL: str = "deepseek-chat-33b"
    
    # Base de données
    DATABASE_URL: str
    REDIS_URL: str
    
    # Sécurité
    JWT_SECRET: str
    ENCRYPTION_KEY: str
    ALLOWED_HOSTS: list = ["yourdomain.com"]
    
    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    
    # AWS (pour backups)
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    S3_BUCKET: str
    
    # Monitoring
    SENTRY_DSN: str
    PROMETHEUS_PORT: int = 9090
    
    class Config:
        env_file = ".env.production" 