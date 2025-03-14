from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql://user:password@localhost/deepstudy"
        )
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        self.Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Instance globale de la base de données
db = Database() 