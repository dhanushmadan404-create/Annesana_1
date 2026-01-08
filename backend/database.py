# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ---------------- DATABASE URL ----------------
# Fetch from Render environment variables
DATABASE_URL = os.getenv("DATABASE_URL")  # Render sets this in the dashboard

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# ---------------- ENGINE ----------------
engine = create_engine(
    DATABASE_URL,
    echo=True,            # Set to True for debug SQL queries
    pool_pre_ping=True
)

# ---------------- SESSION ----------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------- BASE ----------------
Base = declarative_base()

# ---------------- CREATE TABLES ----------------
def init_db():
    import fastapi_models  # import all models
    Base.metadata.create_all(bind=engine)
