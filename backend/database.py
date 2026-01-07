from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

# If DATABASE_URL is missing, we don't want the server to crash on startup.
# Instead, we handle it gracefully.
if db_url:
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
else:
    engine = None
    SessionLocal = None

Base = declarative_base()

def get_db():
    if not SessionLocal:
        raise ValueError("❌ DATABASE_URL is not set. Please add it to Vercel Environment Variables.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
