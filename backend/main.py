from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Include all routers with a common /api prefix
app.include_router(user.router, prefix="/api")
app.include_router(food.router, prefix="/api")
app.include_router(vendor.router, prefix="/api")

# We removed the @app.get("/") because Vercel serves the static index.html directly.
