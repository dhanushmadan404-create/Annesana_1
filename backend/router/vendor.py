from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import time

import os
import base64
import uuid

from database import get_db
from core.security import get_current_user
from models.user import User
from models.vendor import Vendor
from schemas.vendor import VendorResponse

router = APIRouter(prefix="/vendors", tags=["Vendors"])

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
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return f"/uploads/{filename}"

# ================= CREATE VENDOR =================
@router.post("", response_model=VendorResponse)
def create_vendor(
    phone_number: str = Form(...),
    opening_time: time = Form(...),
    closing_time: time = Form(...),
    cart_image_base64: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if db.query(Vendor).filter(Vendor.user_id == current_user.user_id).first():
        raise HTTPException(status_code=400, detail="Vendor already exists")

    vendor = Vendor(
        phone_number=phone_number,
        opening_time=opening_time,
        closing_time=closing_time,
        cart_image_url=save_base64_image(cart_image_base64),
        user_id=current_user.user_id
    )

    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor

# ================= GET ALL VENDORS =================
@router.get("", response_model=List[VendorResponse])
def get_all_vendors(db: Session = Depends(get_db)):
    return db.query(Vendor).all()

# ================= GET VENDOR BY ID =================
@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

# ================= GET MY VENDOR =================
@router.get("/me", response_model=VendorResponse)
def get_my_vendor(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor = db.query(Vendor).filter(Vendor.user_id == current_user.user_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

# ================= UPDATE VENDOR =================
@router.put("", response_model=VendorResponse)
def update_vendor(
    phone_number: str | None = Form(None),
    opening_time: time | None = Form(None),
    closing_time: time | None = Form(None),
    cart_image_base64: str | None = Form(None),
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

# ================= DELETE VENDOR =================
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
