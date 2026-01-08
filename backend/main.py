from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
import os
import sys
import logging

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- PATH FIX ----------------
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# ---------------- ROUTERS ----------------
from .router import user, food, vendor, auth   # 👈 ADD auth

# ---------------- APP ----------------
app = FastAPI(title="Annesana API")

# ---------------- EXCEPTION HANDLERS ----------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"CRITICAL ERROR: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error_type": type(exc).__name__
        }
    )

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- STATIC FILES (IMAGES) ----------------
# 🔥 THIS FIXES IMAGE NOT SHOWING
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ---------------- ROUTERS (API PREFIX ONLY) ----------------
# ✅ Vercel safe
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(food.router, prefix="/api")
app.include_router(vendor.router, prefix="/api")

# ---------------- HEALTH ----------------
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}

@app.get("/")
def home():
    return {"message": "Welcome to Annesana API."}
