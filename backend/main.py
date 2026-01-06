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

# Include all routers
app.include_router(user.router)
app.include_router(food.router)
app.include_router(vendor.router)

# We removed the @app.get("/") because Vercel serves the static index.html directly.
