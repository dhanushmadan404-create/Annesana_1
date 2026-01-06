from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import all routers
from router import user, food, vendor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(user.router)
app.include_router(food.router)
app.include_router(vendor.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}
