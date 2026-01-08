# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ---------------- DATABASE URL ----------------
DATABASE_URL = os.getenv("DATABASE_URL")  # must be set in Render/Env

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# ---------------- ENGINE & SESSION ----------------
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------- DEPENDENCY ----------------
# This is what your routers expect
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- INIT TABLES ----------------
def init_db():
    import fastapi_models  # import all your models
    Base.metadata.create_all(bind=engine)
