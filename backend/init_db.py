import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Add current directory to path so we can import 'database' and 'fastapi_models'
sys.path.append(os.path.dirname(__file__))

from database import engine, Base
import fastapi_models  # This is crucial! Base needs to know about the models

# Load environment variables
load_dotenv()

def initialize_database():
    print("🚀 Connecting to Supabase...")
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("❌ Error: DATABASE_URL not found in .env file")
        return

    try:
        print("🏗️ Creating tables (users, vendors, foods)...")
        # Base.metadata.create_all will only create tables that don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables initialized successfully!")
        print("Check your Supabase project now, you should see the tables!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    initialize_database()
