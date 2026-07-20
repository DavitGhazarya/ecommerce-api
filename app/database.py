from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# Use the modern psycopg (v3) driver instead of psycopg2 for better
# compatibility on Windows (fixes UnicodeDecodeError issues).
database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
