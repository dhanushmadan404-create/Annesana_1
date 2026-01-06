from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, TIMESTAMP,Text,Numeric,Float,Time
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    user = "user"
    vendor = "vendor"
    admin="admin"

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    password_hash = Column(String, nullable=False)
    name=Column(String,nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    image=Column(Text,nullable=True)


    vendor = relationship("Vendor", back_populates="user", uselist=False)

class Food(Base):
    __tablename__ = "foods"
    
    food_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey("vendors.vendor_id"), nullable=False)
    food_name = Column(String(255), nullable=False)
    food_image_url = Column(String(255))
    category = Column(String(100))
    latitude=Column(Float,nullable=False)
    longitude=Column(Float,nullable=False)
   
    vendor = relationship("Vendor", back_populates="foods")

class Vendor(Base):
    __tablename__ = "vendors"
    
    vendor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_number=Column(String,nullable=False)
    cart_image_url=Column(String,nullable=False)
    opening_time=Column(Time,nullable=False)
    closing_time=Column(Time,nullable=False)
    user_id = Column(
    Integer,
    ForeignKey("users.user_id"),
    nullable=False,
    unique=True   # one user → one vendor
)

    foods = relationship("Food", back_populates="vendor")
    user = relationship("User", back_populates="vendor", uselist=False)
