from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from config import get_user_by_email

from data_base import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Users point
@app.post("/user/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email, models_items=models.User)
    if db_user:
        raise HTTPException(status_code=400, detail="Электронная почта уже зарегистрирована")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), models_items=models.User):
    users = crud.get_items(db, skip=skip, models_items=models_items, limit=limit)
    return users


@app.get("/user/{user_id}", response_model=schemas.UserRead)
def read_user_item(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_item_id(db,
                               item_id=user_id,
                               models_items=models.User,
                               models_items_db=models.User.id,
                               quantity='first')
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user

@app.put("/user/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/user/{user_id}")
def delete_product(user_id: int, db: Session = Depends(get_db)):
    del_item = crud.delete_item(db=db, item_id=user_id, models_item=models.User)
    return {'Пользователь удален из базы': del_item}

# Products point
@app.post("/product/", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=list[schemas.ProductRead])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items_products = crud.get_items(db=db, skip=skip, limit=limit, models_items=models.Product)
    return items_products


@app.get("/product/{product_id}", response_model=schemas.ProductRead)
def read_products_item(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_item_id(db,
                                  item_id=product_id,
                                  models_items=models.Product,
                                  models_items_db=models.Product.id,
                                  quantity='first')
    if db_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return db_product


@app.put("/product/{product_id}", response_model=schemas.ProductRead)
def update_products(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    item_product = crud.update_product(db=db, product_id=product_id, product=product)
    return item_product


@app.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    del_item = crud.delete_item(db=db, item_id=product_id, models_item=models.Product)
    return {'Продукт удален из базы': del_item}


# Orders points
@app.post("/order/{user_id}/{product_id}", response_model=schemas.OrderRead)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.OrderRead])
def read_orders(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db=db, limit=limit, models_items=models.Order)


@app.get("/order/{user_id}", response_model=list[schemas.OrderRead])
def read_order_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_item_id(db=db,
                            item_id=user_id,
                            models_items=models.Order,
                            models_items_db=models.Order.user_id,
                            quantity='all')

@app.put("/order/{order_id}", response_model=schemas.ProductRead)
def update_products(order_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.update_order(db=db, order_id=order_id, order=order)

@app.delete("/order/{order_id}}")
def delete_product(order_id: int, db: Session = Depends(get_db)):
    del_item = crud.delete_item(db=db, item_id=order_id, models_item=models.Order)
    return {'Заказ удален из базы': del_item}
