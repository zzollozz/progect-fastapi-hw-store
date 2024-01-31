"""
import re
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, constr, EmailStr, field_validator

"""
##########
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import relationship

from data_base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items_user = relationship("Order", back_populates="owner_user")

    def __str__(self):
        return f"table_users"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name_product = Column(String(100))
    description = Column(Text())
    price = Column(Float)

    items_product = relationship("Order", back_populates="owner_product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    owner_user = relationship("User", back_populates="items_user")
    owner_product = relationship("Product", back_populates="items_product")


