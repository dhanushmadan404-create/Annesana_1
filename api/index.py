import sys
import os

# Get the absolute path of the backend folder
current_dir = os.path.dirname(__file__)
backend_path = os.path.abspath(os.path.join(current_dir, "..", "backend"))

# Add the backend folder to sys.path
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Import the FastAPI 'app' from main.py
try:
    from main import app
except ImportError as e:
    print(f"❌ Error importing app: {e}")
    raise

# Vercel needs the app object to be available as 'app'
app = app
