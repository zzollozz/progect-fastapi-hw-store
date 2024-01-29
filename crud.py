from datetime import datetime
from sqlalchemy.orm import Session

import models
import schemas
from config import set_password


def create_user(db: Session, user: schemas.UserCreate):
    """Регистрация нового пользователя в БД"""

    new_user = models.User(first_name=user.first_name,
                           last_name=user.last_name,
                           email=user.email,
                           hashed_password=set_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_product(db: Session, product: schemas.ProductCreate):
    """Создание нового продукта в БД"""
    new_product = models.Product(name_product=product.name_product,
                                 description=product.description,
                                 price=product.price
                                 )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def create_order(db: Session, order: schemas.OrderCreate):
    """Создание заказа"""
    new_order = models.Order(user_id=order.user_id,
                             product_id=order.product_id,
                             order_date=datetime.now(),
                             is_active=True)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_items(db: Session, models_items, skip: int = 0, limit: int = 100):
    """Вывод всех зарегистрированных пользователей в БД"""
    return db.query(models_items).offset(skip).limit(limit).all()


def get_item_id(db: Session, item_id: int, models_items, models_items_db, quantity):
    if quantity == 'first':
        return db.query(models_items).filter(models_items_db == item_id).first()
    elif quantity == 'all':
        return db.query(models_items).filter(models_items_db == item_id).all()
    else:
        raise ValueError('Invalid quantity')


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    """Обновление данных о пользователе в БД"""
    old_item = db.query(models.User).filter(models.User.id == user_id).first()

    old_item.first_name = user.first_name
    old_item.last_name = user.last_name
    old_item.email = user.email
    old_item.password = user.password

    db.add(old_item)
    db.commit()
    db.refresh(old_item)
    return old_item


def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    """Обновление данных о продукте в БД"""
    old_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    old_product.name_product = product.name_product
    old_product.description = product.description
    old_product.price = product.price

    db.add(old_product)
    db.commit()
    db.refresh(old_product)
    return old_product


def update_order(db: Session, order_id: int, order: schemas.OrderCreate):
    old_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    old_order.user_id = order.user_id
    old_order.product_id = order.product_id
    old_order.order_date = datetime.now()
    old_order.is_active = order.order_status

    db.add(old_order)
    db.commit()
    db.refresh(old_order)
    return old_order

def delete_item(db: Session, item_id: int, models_item):
    item_product = db.query(models_item).filter(models_item.id == item_id).first()

    db.delete(item_product)
    db.commit()
    return item_product
