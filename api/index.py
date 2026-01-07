import os
import sys

# Define the root of the project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

# Add the project root and backend dir to sys.path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Import the app using a standard import
try:
    from backend.main import app
except ImportError:
    # Fallback for different directory contexts
    from main import app

# Vercel needs 'app' to be exposed
app = app
