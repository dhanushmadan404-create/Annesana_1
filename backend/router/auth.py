from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..fastapi_models import User
from ..core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or user.password_hash != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.user_id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.user_id,
            "name": user.name,
            "email": user.email
        }
    }
