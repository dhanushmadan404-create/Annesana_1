# ==================== routers/food.py ====================
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import fastapi_schemas
import fastapi_models
from database import get_db

import os
import tempfile
import string

# ---------------- UTILS ----------------
BASE62_ALPHABET = string.digits + string.ascii_letters

def base62_decode(s: str) -> int:
    if not s: return 0
    # Handle plain integers if they are passed instead of strings
    if s.isdigit(): return int(s)
    res = 0
    for char in s:
        try:
            res = res * 62 + BASE62_ALPHABET.index(char)
        except ValueError:
            continue # ignore invalid chars
    return res

try:
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
except OSError:
    UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "uploads")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- ROUTER ----------------
from core.security import get_current_user
from fastapi_models import User

# ---------------- ROUTER ----------------
router = APIRouter(prefix="/foods", tags=["Foods"])

# ---------------- GET LOCATIONS ----------------
@router.get("/locations", response_model=List[fastapi_schemas.FoodResponse])
def get_all_food_locations(db: Session = Depends(get_db)):
    return db.query(fastapi_models.Food).all()

# ---------------- CREATE FOOD ----------------
@router.post("/", response_model=fastapi_schemas.FoodResponse)
def create_food(
    food_name: str = Form(...),
    category: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    vendor_id: str = Form(...),  # Accept Base62 string
    image_base64: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        vendor_id_int = base62_decode(vendor_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid Base62 vendor_id")

    new_food = fastapi_models.Food(
        food_name=food_name,
        food_image_url=image_base64, # Save the Base64 string directly
        category=category,
        latitude=latitude,
        longitude=longitude,
        vendor_id=vendor_id_int
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food

# ---------------- GET FOODS BY CATEGORY ----------------
@router.get("/category/{category_name}", response_model=List[fastapi_schemas.FoodResponse])
def get_foods_by_category(category_name: str, db: Session = Depends(get_db)):
    foods = db.query(fastapi_models.Food).filter(fastapi_models.Food.category == category_name).all()
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found in this category")
    return foods

# ---------------- GET FOODS BY VENDOR ----------------
@router.get("/vendor/{vendor_id}", response_model=List[fastapi_schemas.FoodResponse])
def get_foods_by_vendor(vendor_id: str, db: Session = Depends(get_db)):
    try:
        vendor_id_int = base62_decode(vendor_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid Base62 vendor_id")

    foods = db.query(fastapi_models.Food).filter(fastapi_models.Food.vendor_id == vendor_id_int).all()
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found for this vendor")
    return foods
# -----------------get food by food id -----------------

@router.get("/location/{food_id}")
def get_food_location(food_id: int, db: Session = Depends(get_db)):
    food = db.query(fastapi_models.Food).filter(fastapi_models.Food.food_id == food_id).first()

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    return {
        "food_id": food.food_id,
        "food_name": food.food_name,
        "latitude": food.latitude,
        "longitude": food.longitude
    }
# ---------------- DELETE FOOD BY VENDOR + FOOD NAME ----------------
@router.delete("/vendor/{vendor_id}/food/{food_name}")
def delete_food_by_vendor_and_name(
    vendor_id: str, 
    food_name: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        vendor_id_int = base62_decode(vendor_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid Base62 vendor_id")

    food = (
        db.query(fastapi_models.Food)
        .filter(
            fastapi_models.Food.vendor_id == vendor_id_int,
            fastapi_models.Food.food_name == food_name
        )
        .first()
    )

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    db.delete(food)
    db.commit()

    return {"message": "Food deleted successfully", "vendor_id": vendor_id, "food_name": food_name}

# ---------------- DELETE ALL FOODS BY VENDOR ID ----------------
@router.delete("/vendor/{vendor_id}")
def delete_foods_by_vendor(
    vendor_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        vendor_id_int = base62_decode(vendor_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid Base62 vendor_id")

    foods = db.query(fastapi_models.Food).filter(fastapi_models.Food.vendor_id == vendor_id_int).all()

    if not foods:
        raise HTTPException(status_code=404, detail="No foods found for this vendor")

    for food in foods:
        db.delete(food)

    db.commit()
    return {"message": "All foods deleted for this vendor", "vendor_id": vendor_id, "deleted_count": len(foods)}

# ---------------- DELETE FOOD BY FOOD ID ----------------
@router.delete("/{food_id}")
def delete_food_by_id(
    food_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        food_id_int = base62_decode(food_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid Base62 food_id")

    food = db.query(fastapi_models.Food).filter(fastapi_models.Food.food_id == food_id_int).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    db.delete(food)
    db.commit()
    return {"message": "Food deleted successfully", "food_id": food_id}
