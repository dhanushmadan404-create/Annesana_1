# ==================== routers/vendor.py ====================
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional

import fastapi_models
import fastapi_schemas
from database import get_db

router = APIRouter(prefix="/vendors", tags=["Vendors"])

# ---------------- CREATE VENDOR ----------------
@router.post("/", response_model=fastapi_schemas.VendorResponse)
def create_vendor(
    phone_number: str = Form(...),
    opening_time: str = Form(...),
    closing_time: str = Form(...),
    user_id: int = Form(...),
    cart_image_url: str = Form(...),  # <-- Now just a URL
    db: Session = Depends(get_db)
):
    """
    Create a new vendor with an image URL instead of uploading a file.
    """
    new_vendor = fastapi_models.Vendor(
        phone_number=phone_number,
        cart_image_url=cart_image_url,  # store the URL
        opening_time=opening_time,
        closing_time=closing_time,
        user_id=user_id
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor

# ---------------- GET ALL VENDORS ----------------
@router.get("/", response_model=List[fastapi_schemas.VendorResponse])
def get_all_vendors(db: Session = Depends(get_db)):
    return db.query(fastapi_models.Vendor).all()

# ---------------- GET VENDOR BY ID ----------------
@router.get("/id/{vendor_id}", response_model=fastapi_schemas.VendorResponse)
def get_vendor_by_id(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(fastapi_models.Vendor).filter(fastapi_models.Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

# ---------------- GET VENDOR BY USER ID ----------------
@router.get("/user/{user_id}", response_model=fastapi_schemas.VendorResponse)
def get_vendor_by_user_id(user_id: int, db: Session = Depends(get_db)):
    vendor = db.query(fastapi_models.Vendor).filter(fastapi_models.Vendor.user_id == user_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

@router.get("/check/{user_id}")
def check_vendor(user_id: int, db: Session = Depends(get_db)):
    """
    Returns {'exists': True, 'vendor': ...} or {'exists': False}
    """
    vendor = db.query(fastapi_models.Vendor).filter(fastapi_models.Vendor.user_id == user_id).first()
    if vendor:
        return {"exists": True, "vendor": vendor}
    return {"exists": False}

# ---------------- UPDATE VENDOR ----------------
@router.put("/{vendor_id}", response_model=fastapi_schemas.VendorResponse)
def update_vendor(
    vendor_id: int,
    updated_vendor: fastapi_schemas.VendorCreate,
    db: Session = Depends(get_db)
):
    vendor = db.query(fastapi_models.Vendor).filter(fastapi_models.Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    vendor.phone_number = updated_vendor.phone_number
    vendor.cart_image_url = updated_vendor.cart_image_url
    vendor.opening_time = updated_vendor.opening_time
    vendor.closing_time = updated_vendor.closing_time
    vendor.user_id = updated_vendor.user_id

    db.commit()
    db.refresh(vendor)
    return vendor

# ---------------- DELETE VENDOR ----------------
@router.delete("/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(fastapi_models.Vendor).filter(fastapi_models.Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    db.delete(vendor)
    db.commit()
    return {"message": "Vendor deleted successfully"}
