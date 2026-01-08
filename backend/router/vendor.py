# ==================== routers/vendor.py ====================
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List

import os
import base64
import uuid
import tempfile

from database import get_db
from core.security import get_current_user
from fastapi_models import User, Vendor
import fastapi_schemas

router = APIRouter(prefix="/vendors", tags=["Vendors"])

# ---------------- IMAGE STORAGE (same as user) ----------------
# Vercel has a read-only filesystem except for /tmp
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_base64_image(base64_string: str) -> str:
    try:
        header, encoded = base64_string.split(",", 1)
    except ValueError:
        encoded = base64_string

    image_bytes = base64.b64decode(encoded)
    filename = f"{uuid.uuid4().hex}.png"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return f"/uploads/{filename}"

# ---------------- CREATE VENDOR ----------------
@router.post("", response_model=fastapi_schemas.VendorResponse)
def create_vendor(
    phone_number: str = Form(...),
    opening_time: str = Form(...),
    closing_time: str = Form(...),
    cart_image_base64: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # one user → one vendor
    existing_vendor = db.query(Vendor).filter(Vendor.user_id == current_user.user_id).first()
    if existing_vendor:
        raise HTTPException(status_code=400, detail="Vendor already exists for this user")

    image_url = save_base64_image(cart_image_base64)

    new_vendor = Vendor(
        phone_number=phone_number,
        cart_image_url=image_url,
        opening_time=opening_time,
        closing_time=closing_time,
        user_id=current_user.user_id
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor

# ---------------- GET ALL VENDORS ----------------
@router.get("/", response_model=List[fastapi_schemas.VendorResponse])
def get_all_vendors(db: Session = Depends(get_db)):
    return db.query(Vendor).all()

# ---------------- GET VENDOR BY ID ----------------
@router.get("/{vendor_id}", response_model=fastapi_schemas.VendorResponse)
def get_vendor_by_id(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

# ---------------- GET VENDOR BY LOGGED USER ----------------
@router.get("/me", response_model=fastapi_schemas.VendorResponse)
def get_my_vendor(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor = db.query(Vendor).filter(Vendor.user_id == current_user.user_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

# ---------------- UPDATE VENDOR ----------------
@router.put("", response_model=fastapi_schemas.VendorResponse)
def update_vendor(
    phone_number: str = Form(None),
    opening_time: str = Form(None),
    closing_time: str = Form(None),
    cart_image_base64: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor = db.query(Vendor).filter(Vendor.user_id == current_user.user_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    if phone_number:
        vendor.phone_number = phone_number
    if opening_time:
        vendor.opening_time = opening_time
    if closing_time:
        vendor.closing_time = closing_time
    if cart_image_base64:
        vendor.cart_image_url = save_base64_image(cart_image_base64)

    db.commit()
    db.refresh(vendor)
    return vendor

# ---------------- DELETE VENDOR ----------------
@router.delete("")
def delete_vendor(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor = db.query(Vendor).filter(Vendor.user_id == current_user.user_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    db.delete(vendor)
    db.commit()
    return {"message": "Vendor deleted successfully"}
