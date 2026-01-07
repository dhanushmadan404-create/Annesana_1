from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Standard setup for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import routers safely
from router import user, food, vendor

app = FastAPI(title="Annesana API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion under /api prefix matches frontend exactly
app.include_router(user.router, prefix="/api")
app.include_router(food.router, prefix="/api")
app.include_router(vendor.router, prefix="/api")

# Add roots without /api just in case Vercel rewrites differently
app.include_router(user.router)
app.include_router(food.router)
app.include_router(vendor.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}

@app.get("/")
def home():
    return {"message": "Welcome to Annesana API."}

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    return {
        "error": "Route not found",
        "path_received": path_name,
        "method": request.method,
        "full_url": str(request.url)
    }
