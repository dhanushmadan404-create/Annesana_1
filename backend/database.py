# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------- DATABASE URL ----------------
# Render sets the DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL")  # ensure this exists in Render env

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set!")

# ---------------- ENGINE & SESSION ----------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ---------------- DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
