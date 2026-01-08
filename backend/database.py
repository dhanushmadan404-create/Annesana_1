from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

# Handle Vercel's potentially outdated postgres:// prefix
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if db_url:
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
else:
    engine = None
    SessionLocal = None

Base = declarative_base()

def get_db():
    if not db_url:
        raise ValueError("❌ DATABASE_URL is not set in environment variables.")
    
    if not SessionLocal:
        raise ValueError("❌ Database SessionLocal not initialized.")
    
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Database error: {e}")
        raise e
    finally:
        db.close()
