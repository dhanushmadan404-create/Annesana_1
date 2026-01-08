from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db

from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from fastapi_models import User
from fastapi_schemas import UserResponse, LoginResponse

from pydantic import BaseModel
import os
import tempfile
import base64
import uuid

# ---------------- ROUTER ----------------
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ---------------- IMAGE STORAGE ----------------
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

# ---------------- CREATE USER ----------------
@router.post("", response_model=UserResponse)
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    image_base64: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check email already exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    image_url = save_base64_image(image_base64)

    new_user = User(
        name=name,
        email=email,
        role=role,
        image=image_url,
        password_hash=hash_password(password),
        created_at=datetime.utcnow()
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Registration failed")

# ---------------- LOGIN ----------------
class LoginData(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=LoginResponse)
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.user_id,
            "role": str(user.role.value) if hasattr(user.role, "value") else str(user.role)
        }
    )

    return LoginResponse(
        user_id=user.user_id,
        email=user.email,
        name=user.name,
        image=user.image,
        role=user.role,
        created_at=user.created_at,
        access_token=access_token,
        token_type="bearer"
    )

# ---------------- GET CURRENT USER ----------------
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# ---------------- GET USER BY ID ----------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# ---------------- UPDATE PROFILE ----------------
@router.put("/profile", response_model=UserResponse)
def update_profile(
    name: str = Form(None),
    image_base64: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if name:
        current_user.name = name

    if image_base64:
        image_url = save_base64_image(image_base64)
        current_user.image = image_url

    db.commit()
    db.refresh(current_user)
    return current_user
