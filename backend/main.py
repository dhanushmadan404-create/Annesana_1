from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Ensure this script's directory is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import routers
# Using standard imports since current_dir is in sys.path
from router import user, food, vendor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with the /api prefix for Vercel routing
app.include_router(user.router, prefix="/api")
app.include_router(food.router, prefix="/api")
app.include_router(vendor.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}

@app.get("/")
def home():
    return {"message": "Welcome to Annesana API"}
