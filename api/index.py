import os
import sys

# Add project root and backend dir to sys.path for robust imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_dir = os.path.join(project_root, "backend")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from backend.main import app
except ImportError:
    # Fallback for environments where 'backend' is the relative root
    from main import app

# Vercel looks for the variable 'app' in this file
app = app
