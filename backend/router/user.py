from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from core.security import hash_password, verify_password, create_access_token, get_current_user
from fastapi_models import User
from fastapi_schemas import UserResponse, LoginResponse, UserCreate
import os
import tempfile
from pydantic import BaseModel, ValidationError

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("", response_model=UserResponse)
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    image_base64: str = Form(...),
    db: Session = Depends(get_db)
):
    # Manual validation for Form data using Pydantic
    try:
        # Check if email exists
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

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
        db.rollback()
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

# --- Login Logic ---
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

    # Create token for session
    access_token = create_access_token(data={
        "sub": user.email, 
        "user_id": user.user_id, 
        "role": str(user.role.value) if hasattr(user.role, 'value') else str(user.role)
    })
    
    # Prepare response
    user.access_token = access_token
    return user

@router.get("/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/profile", response_model=UserResponse)
@router.put("/users/profile/", response_model=UserResponse)
def update_profile(
    name: str = Form(None),
    image_base64: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if name:
        current_user.name = name
    if image_base64:
        current_user.image = image_base64

    db.commit()
    db.refresh(current_user)
    return current_user
