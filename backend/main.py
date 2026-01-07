from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Ensure this script's directory is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import routers
from router import user, food, vendor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers with and without prefix
# This guarantees that /api/users and /users both work
for prefix in ["/api", ""]:
    app.include_router(user.router, prefix=prefix)
    app.include_router(food.router, prefix=prefix)
    app.include_router(vendor.router, prefix=prefix)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}

@app.get("/")
def home():
    return {"message": "Welcome to Annesana API"}

# ✅ Catch-all for debugging 404s
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    return {
        "error": "Route not found",
        "path_received": path_name,
        "method": request.method,
        "full_url": str(request.url)
    }
