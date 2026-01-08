from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Standard setup for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import routers safely
from router import user, food, vendor

app = FastAPI(title="Annesana API")

# Global Exception Handler for 500s
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    logger.error(f"Global error caught: {error_msg}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error_type": type(exc).__name__,
            "message": error_msg 
        }
    )

# Override default validation error handler to be more specific if needed
from fastapi.exceptions import RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

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

# Also include without prefix just as fallback for local testing if needed
# but Vercel will mostly use the /api prefix versions via the rewrite
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
