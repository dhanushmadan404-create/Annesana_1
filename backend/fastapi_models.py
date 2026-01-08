# ==================== fastapi_models.py ====================

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,
    Text,
    Float,
    Time
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

# -------------------------------------------------
# Roles (optional, not enforced)
# -------------------------------------------------
class UserRole(str, enum.Enum):
    user = "user"
    vendor = "vendor"
    admin = "admin"

# -------------------------------------------------
# User
# -------------------------------------------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.utcnow
    )
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # keep string (Vercel safe)
    image = Column(Text, nullable=True)

    vendor = relationship(
        "Vendor",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
    )

# -------------------------------------------------
# Vendor
# -------------------------------------------------
class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_number = Column(String, nullable=False)
    cart_image_url = Column(Text, nullable=False)

    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    foods = relationship(
        "Food",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )

    user = relationship(
        "User",
        back_populates="vendor",
        uselist=False
    )

# -------------------------------------------------
# Food
# -------------------------------------------------
class Food(Base):
    __tablename__ = "foods"

    food_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vendor_id = Column(
        Integer,
        ForeignKey("vendors.vendor_id", ondelete="CASCADE"),
        nullable=False
    )

    food_name = Column(String(255), nullable=False)
    food_image_url = Column(Text)
    category = Column(String(100))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    vendor = relationship(
        "Vendor",
        back_populates="foods"
    )
