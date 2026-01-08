import os
import sys
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Add project root and backend dir to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_dir = os.path.join(project_root, "backend")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

app = None
startup_error = None

try:
    from backend.main import app as fastapi_app
    app = fastapi_app
except Exception as e:
    startup_error = {
        "error": str(e),
        "traceback": traceback.format_exc(),
        "path": sys.path
    }

# If the app failed to load, create a fallback app to report the error
if app is None:
    app = FastAPI()
    
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all_error(path: str):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Startup Error",
                "message": startup_error.get("error") if startup_error else "Unknown error",
                "debug": startup_error
            }
        )

# Vercel entry point
app = app
