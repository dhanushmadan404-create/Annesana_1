from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from core.security import hash_password, verify_password, create_access_token
from fastapi_models import User
from fastapi_schemas import UserResponse, LoginResponse
import os
import tempfile
from pydantic import BaseModel

router = APIRouter(tags=["Users"])

# Support both with and without trailing slash for all user routes
@router.post("/users", response_model=UserResponse)
@router.post("/users/", response_model=UserResponse)
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    image_base64: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if email is already taking
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # The role in DB is Enum, but string should automatically convert
    try:
        db_user = User(
            name=name,
            email=email,
            role=role, 
            image=image_base64,
            password_hash=hash_password(password),
            created_at=datetime.utcnow()
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"❌ Database error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# --- Login Logic ---
class LoginData(BaseModel):
    email: str
    password: str

@router.post("/users/login", response_model=LoginResponse)
@router.post("/users/login/", response_model=LoginResponse)
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")

    # Create token for session
    access_token = create_access_token(data={
        "sub": user.email, 
        "user_id": user.user_id, 
        "role": str(user.role.value) if hasattr(user.role, 'value') else str(user.role)
    })
    
    # Prepare response
    user.access_token = access_token
    return user

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/profile", response_model=UserResponse)
@router.put("/users/profile/", response_model=UserResponse)
def update_profile(
    email: str = Form(...),
    name: str = Form(None),
    image_base64: str = Form(None),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if name:
        user.name = name
    if image_base64:
        user.image = image_base64

    db.commit()
    db.refresh(user)
    return user
