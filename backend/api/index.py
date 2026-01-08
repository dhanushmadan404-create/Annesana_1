# entrypoint.py or index.py (depending on Vercel/Render)
import os
import sys
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# ---------------- PATH FIX ----------------
# Add project root and backend dir to sys.path for absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_dir = os.path.join(project_root, "backend")

for p in [project_root, backend_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ---------------- APP LOAD ----------------
app = None
startup_error = None

try:
    # Import FastAPI app from backend/main.py
    from backend.main import app as fastapi_app
    app = fastapi_app
except Exception as e:
    startup_error = {
        "error": str(e),
        "traceback": traceback.format_exc(),
        "sys_path": sys.path,
    }

# ---------------- FALLBACK APP ----------------
if app is None:
    app = FastAPI(title="Startup Error App")

    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def catch_all_error(path: str):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Startup Error",
                "message": startup_error.get("error") if startup_error else "Unknown error",
                "debug": startup_error,
            },
        )

# ---------------- EXPORT ----------------
# Standard entry point for deployment platforms
app = app
