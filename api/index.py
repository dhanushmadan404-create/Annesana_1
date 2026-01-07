import sys
import os

# 1. Get the path to 'backend' directory
# Since this file is in 'api/', backend is in '../backend'
current_file_path = os.path.abspath(__file__)
api_dir = os.path.dirname(current_file_path)
root_dir = os.path.abspath(os.path.join(api_dir, ".."))
backend_path = os.path.join(root_dir, "backend")

# 2. Add backend and api to sys.path
if backend_path not in sys.path:
    sys.path.append(backend_path)
if api_dir not in sys.path:
    sys.path.append(api_dir)

# 3. Import the FastAPI app from backend/main.py
try:
    from main import app
except ImportError as e:
    # If standard import fails, try relative or direct
    try:
        from backend.main import app
    except ImportError:
        print(f"❌ Critical Error: Could not import 'app' from main.py. Path: {backend_path}")
        raise e

# 4. Mandatory for Vercel: expose the app variable
app = app
