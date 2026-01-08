import subprocess
import sys
import os

def setup_database():
    print("🚀 Starting Annesana Database Setup...")
    
    # Check if .env exists
    env_path = os.path.join("backend", ".env")
    if not os.path.exists(env_path):
        print("❌ Error: backend/.env file not found!")
        print("Please create it with your DATABASE_URL.")
        return

    # Run the init_db module
    print("🏗️  Initializing tables in Supabase...")
    try:
        # We use -m to handle relative imports correctly
        result = subprocess.run(
            [sys.executable, "-m", "backend.init_db"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("❌ Initialization failed:")
            print(result.stderr)
        else:
            print("✅ Database is ready!")
            
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    setup_database()
