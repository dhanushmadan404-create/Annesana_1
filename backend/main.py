from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
import os

# Import all routers
from router import user, food, vendor

# Create FastAPI application instance
app = FastAPI()

# # make sure uploads folder exists
# os.makedirs("uploads", exist_ok=True)

# # mount the uploads folder
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = [
    "http://127.0.0.1:5501",  # your frontend origin
    "http://localhost:5501"
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# app.mount("/static", StaticFiles(directory="/frontend"), name="static")
# for modify the request before request

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel/Testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include all routers with API prefix
app.include_router(user.router)
app.include_router(food.router)
app.include_router(vendor.router)
