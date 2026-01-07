import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("❌ Error: DATABASE_URL not found in .env file")
    exit()

# Create connection
engine = create_engine(db_url)

def upgrade_database():
    print("🛠️ Starting database upgrade...")
    
    commands = [
        # Change cart_image_url in vendors table to TEXT
        "ALTER TABLE vendors ALTER COLUMN cart_image_url TYPE TEXT;",
        # Change food_image_url in foods table to TEXT
        "ALTER TABLE foods ALTER COLUMN food_image_url TYPE TEXT;",
        # Also ensure user image is TEXT just in case
        "ALTER TABLE users ALTER COLUMN image TYPE TEXT;"
    ]
    
    with engine.connect() as conn:
        for cmd in commands:
            try:
                print(f"Running: {cmd}")
                conn.execute(text(cmd))
                conn.commit()
                print("✅ Success")
            except Exception as e:
                print(f"⚠️ Notice: {e}")
                print("Continuing to next command...")

    print("\n✨ Database upgrade finished. Try registering again!")

if __name__ == "__main__":
    upgrade_database()
