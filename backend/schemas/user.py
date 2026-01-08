from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    vendor = "vendor"
    admin = "admin"

class UserBase(BaseModel):
    email: str
    name: str
    image: str | None
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
