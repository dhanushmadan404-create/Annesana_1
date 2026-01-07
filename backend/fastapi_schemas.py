from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime, time
from typing import Optional
from enum import Enum

# Define Role Enum for Pydantic
class UserRole(str, Enum):
    user = "user"
    vendor = "vendor"
    admin = "admin"

# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=100)
    image: Optional[str] = None
    role: UserRole

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class LoginResponse(UserResponse):
    access_token: str
    token_type: str = "bearer"

# ==================== REVIEW SCHEMAS ====================
class ReviewBase(BaseModel):
    user_id: int
    food_id: int
    rating: int = Field(..., ge=1, le=5)
    review_text: str = Field(..., min_length=1)

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    review_id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ==================== FOOD SCHEMAS ====================
class FoodBase(BaseModel):
    food_name: str = Field(..., min_length=1)
    food_image_url: str
    category: str
    latitude: float
    longitude: float
    vendor_id: int

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    food_id: int
    model_config = ConfigDict(from_attributes=True)


# ==================== VENDOR SCHEMAS ====================
class VendorBase(BaseModel):
    phone_number: str = Field(..., pattern=r"^\d{10}$")
    cart_image_url: str
    opening_time: time
    closing_time: time
    user_id: int

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    vendor_id: int 
    model_config = ConfigDict(from_attributes=True)
