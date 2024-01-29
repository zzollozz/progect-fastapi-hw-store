import re
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, field_validator


class UserBase(BaseModel):
    first_name: str = Field(description='Фамилия')
    last_name: str = Field(description='Имя')
    email: EmailStr = Field(description='email', examples=['marcelo@mail.com'])

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not bool(re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', value)):
            raise ValueError("Электронная почта недействительна")
        return value


class UserCreate(UserBase):
    password: str = Field(description='password', min_length=6)


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name_product: str = Field(description='Название продукта')
    description: str = Field(description='Описание')
    price: float = Field(description='Цена')


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime
    order_status: bool = True


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int

    class Config:
        orm_mode = True
