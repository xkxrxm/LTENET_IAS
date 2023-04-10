from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, CheckConstraint, text
from sqlalchemy.orm import relationship
from typing import Optional

from .database import Base


class User(Base):
    __tablename__ = "User"

    username = Column(String, primary_key=True, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
