from fastapi import APIRouter, Depends,UploadFile,File,Form, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from core.security import hash_password
from fastapi_models import User
from fastapi_schemas import UserCreate, UserResponse
from core.security import verify_password
import shutil, os
router = APIRouter(prefix="/users", tags=["Users"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=UserResponse)
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # check if email exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # save image
    image_name = f"{datetime.utcnow().timestamp()}_{image.filename}"
    image_path = os.path.join(UPLOAD_DIR, image_name)
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # create user
    db_user = User(
        name=name,
        email=email,
        role=role,
        image=image_path,
        password_hash=hash_password(password),
        created_at=datetime.utcnow()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
# ----------------------------change and validation
from pydantic import BaseModel
from typing import Optional
class LoginData(BaseModel):
    email: str
    password: str


class ProfileUpdate(BaseModel):
    email: str
    name: Optional[str] = None
    image: Optional[str] = None

# get all user
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# ---------------- GET VENDOR BY ID ----------------
@router.get("/{user_id}", response_model=UserResponse)
def get_vendor_by_id(user_id: int, db: Session = Depends(get_db)):
    user= (
        db.query(User)
        .filter(User.user_id ==  user_id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user

# login
@router.post("/login", response_model=UserResponse)
def login(data: LoginData, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email not registered"
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    return user

def update_profile(data: ProfileUpdate, db: Session = Depends(get_db)):

    # find user by email
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email not registered"
        )

    # update fields if provided
    if data.name is not None:
        user.name = data.name

    if data.image is not None:
        user.image = data.image

    db.commit()
    db.refresh(user)

    return user


# update the user name and image platform
@router.put("/profile", response_model=UserResponse)
def update_profile(
    email: str = Form(...),
    name: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if name:
        user.name = name

    if image:
        file_path = f"uploads/{image.filename}"
        with open(file_path, "wb") as f:
            f.write(image.file.read())
        user.image = file_path

    db.commit()
    db.refresh(user)
    return user

