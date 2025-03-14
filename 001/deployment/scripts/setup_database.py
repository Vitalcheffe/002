import asyncio
from sqlalchemy import create_engine
from alembic import command
from alembic.config import Config
import os

async def setup_database():
    """Configure la base de données en production"""
    try:
        # Configuration Alembic
        alembic_cfg = Config("alembic.ini")
        
        # Exécution des migrations
        command.upgrade(alembic_cfg, "head")
        
        # Création des index
        engine = create_engine(os.getenv("DATABASE_URL"))
        with engine.connect() as conn:
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_analysis_user_id ON analyses(user_id);
            """)
            
        print("✅ Base de données configurée avec succès")
    except Exception as e:
        print(f"❌ Erreur configuration DB: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(setup_database()) 