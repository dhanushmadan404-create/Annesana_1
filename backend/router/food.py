



# ==================== routers/food.py ====================
from fastapi import APIRouter, Depends, HTTPException,Form,File,UploadFile
from sqlalchemy.orm import Session
from typing import List
import fastapi_schemas
import fastapi_models
from database import get_db

router = APIRouter(prefix="/foods", tags=["Foods"])

# ---------------- GET LOCATIONS ----------------
@router.get("/locations", response_model=List[fastapi_schemas.FoodResponse])
def get_all_food_locations(db: Session = Depends(get_db)):
    # You might want to filter only foods with lat/lng, but schema enforces it somewhat
    return db.query(fastapi_models.Food).all()

# ---------------- CREATE FOOD ----------------

@router.post("", response_model=fastapi_schemas.FoodResponse)
def create_food(
    food_name: str = Form(...),
    category: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    vendor_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # save image
    image_path = f"uploads/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(image.file.read())

    new_food = fastapi_models.Food(
        food_name=food_name,
        food_image_url=image_path,
        category=category,
        latitude=latitude,
        longitude=longitude,
        vendor_id=vendor_id
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
def get_foods_by_vendor(vendor_id: int, db: Session = Depends(get_db)):
    foods = db.query(fastapi_models.Food).filter(fastapi_models.Food.vendor_id == vendor_id).all()
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found for this vendor")
    return foods


# ---------------- DELETE FOOD BY VENDOR + FOOD NAME ----------------
@router.delete("/vendor/{vendor_id}/food/{food_name}")
def delete_food_by_vendor_and_name(
    vendor_id: int,
    food_name: str,
    db: Session = Depends(get_db)
):
    food = (
        db.query(fastapi_models.Food)
        .filter(
            fastapi_models.Food.vendor_id == vendor_id,
            fastapi_models.Food.food_name == food_name
        )
        .first()
    )

  

    db.delete(food)
    db.commit()

    return {
        "message": "Food deleted successfully",
        "vendor_id": vendor_id,
        "food_name": food_name
    }


# ---------------- DELETE ALL FOODS BY VENDOR ID ----------------
@router.delete("/vendor/{vendor_id}")
def delete_foods_by_vendor(vendor_id: int, db: Session = Depends(get_db)):
    foods = (
        db.query(fastapi_models.Food)
        .filter(fastapi_models.Food.vendor_id == vendor_id)
        .all()
    )

    if not foods:
        raise HTTPException(
            status_code=404,
            detail="No foods found for this vendor"
        )

    for food in foods:
        db.delete(food)

    db.commit()

    return {
        "message": "All foods deleted for this vendor",
        "vendor_id": vendor_id,
        "deleted_count": len(foods)
    }


# ---------------- DELETE FOOD BY ID ----------------
@router.delete("/{food_id}")
def delete_food_by_id(food_id: int, db: Session = Depends(get_db)):
    food = db.query(fastapi_models.Food).filter(fastapi_models.Food.food_id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    db.delete(food)
    db.commit()
    return {"message": "Food deleted successfully"}
