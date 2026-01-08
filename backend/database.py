# ==================== database.py ====================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from fastapi import HTTPException

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# Fix postgres:// → postgresql:// for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

# -------------------------------------------------
# SQLAlchemy engine (Vercel safe)
# -------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # VERY important for Vercel
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# -------------------------------------------------
# Dependency
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )
    finally:
        db.close()
