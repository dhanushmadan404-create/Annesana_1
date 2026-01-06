from pydantic import BaseModel,ConfigDict
from datetime import datetime,time
from typing import Optional
from enum import Enum

# Define Role Enum for Pydantic
class UserRole(str, Enum):
    user = "user"
    vendor = "vendor"
    admin="admin"

# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    email: str
    name:str
    image:str
    role: UserRole

class UserCreate(UserBase):
    password: str
    # created_at should be handled by server, not client
    # so we generally don't include it here

class UserResponse(UserBase):
    user_id: int
    created_at: datetime  # response includes created_at
    # DO NOT include password here

    model_config = ConfigDict(from_attributes=True)


# ==================== REVIEW SCHEMAS ====================
class ReviewBase(BaseModel):
    user_id: int
    food_id: int
   
    rating: int
    review_text: str

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    review_id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== FOOD SCHEMAS ====================
class FoodBase(BaseModel):
    food_name: str
    food_image_url: str
    category: str
    latitude:float
    longitude:float
    vendor_id: int

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    food_id: int

    
    model_config = ConfigDict(from_attributes=True)


# ==================== VENDOR SCHEMAS ====================
class VendorBase(BaseModel):
    phone_number: int
    cart_image_url:str
    opening_time:time
    closing_time:time
    user_id:int

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    vendor_id: int 
    model_config = ConfigDict(from_attributes=True)


