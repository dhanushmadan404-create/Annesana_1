import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from .database import engine, Base
from . import fastapi_models 

# Load environment variables
load_dotenv()

def initialize_database():
    print("🚀 Connecting to Supabase...")
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("❌ Error: DATABASE_URL not found in .env file")
        return

    try:
        print("🏗️ Creating or updating tables...")
        # Step 1: Create missing tables
        Base.metadata.create_all(bind=engine)
        
        # Step 2: Handle the 'role' column transition (Enum -> String)
        # This is the common fix for Role registration errors
        with engine.connect() as conn:
            try:
                # In Postgres, changing Enum to String safely
                print("🔄 Ensuring 'role' column is a text type...")
                conn.execute(text("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR(255);"))
                conn.commit()
                print("✅ Column update successful!")
            except Exception as inner_e:
                print(f"ℹ️ Info: Column might already be String or table is fresh: {inner_e}")

        print("✨ Database is ready!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    initialize_database()
