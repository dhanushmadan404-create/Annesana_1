from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
import base64, uuid, os, string

from database import get_db
from core.security import get_current_user
from models.food import Food
from models.vendor import Vendor
from models.user import User
from schemas.food import FoodResponse

router = APIRouter(prefix="/foods", tags=["Foods"])

# ================= BASE62 =================
BASE62_ALPHABET = string.digits + string.ascii_letters

def base62_decode(s: str) -> int:
    res = 0
    for char in s:
        res = res * 62 + BASE62_ALPHABET.index(char)
    return res

# ================= IMAGE STORAGE =================
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_base64_image(base64_string: str) -> str:
    try:
        _, encoded = base64_string.split(",", 1)
    except ValueError:
        encoded = base64_string

    image_bytes = base64.b64decode(encoded)
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(image_bytes)

    return f"/uploads/{filename}"

# ================= GET ALL FOODS =================
@router.get("", response_model=List[FoodResponse])
def get_all_foods(db: Session = Depends(get_db)):
    return db.query(Food).all()

# ================= CREATE FOOD =================
@router.post("", response_model=FoodResponse)
def create_food(
    food_name: str = Form(...),
    category: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    vendor_id: str = Form(...),
    image_base64: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor_id_int = base62_decode(vendor_id)

    vendor = db.query(Vendor).filter(
        Vendor.vendor_id == vendor_id_int,
        Vendor.user_id == current_user.user_id
    ).first()

    if not vendor:
        raise HTTPException(status_code=403, detail="Not authorized")

    food = Food(
        food_name=food_name,
        category=category,
        latitude=latitude,
        longitude=longitude,
        food_image_url=save_base64_image(image_base64),
        vendor_id=vendor.vendor_id
    )

    db.add(food)
    db.commit()
    db.refresh(food)
    return food

# ================= GET FOOD BY CATEGORY =================
@router.get("/category/{category}", response_model=List[FoodResponse])
def get_foods_by_category(category: str, db: Session = Depends(get_db)):
    foods = db.query(Food).filter(Food.category == category).all()
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found")
    return foods

# ================= GET FOOD BY VENDOR =================
@router.get("/vendor/{vendor_id}", response_model=List[FoodResponse])
def get_foods_by_vendor(vendor_id: str, db: Session = Depends(get_db)):
    vendor_id_int = base62_decode(vendor_id)
    foods = db.query(Food).filter(Food.vendor_id == vendor_id_int).all()
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found")
    return foods

# ================= DELETE FOOD =================
@router.delete("/{food_id}")
def delete_food(
    food_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    food_id_int = base62_decode(food_id)

    food = (
        db.query(Food)
        .join(Vendor)
        .filter(
            Food.food_id == food_id_int,
            Vendor.user_id == current_user.user_id
        )
        .first()
    )

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    db.delete(food)
    db.commit()
    return {"message": "Food deleted successfully"}
