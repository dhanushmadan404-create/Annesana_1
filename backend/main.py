from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import all routers
from router import user, food, vendor

# Create FastAPI application instance
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers with API prefix
app.include_router(user.router)
app.include_router(food.router)
app.include_router(vendor.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

# NOTE: Static files are served by Vercel directly from the /public folder.
# We do not mount them here to avoid 'Directory not found' errors in serverless environments.
