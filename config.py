import hashlib
from settings import salt


def get_user_by_email(db, models_items, email: str):
    """Проверка почты в БД"""
    return db.query(models_items).filter(models_items.email == email).first()

def set_password(user_password):
    return hashlib.sha256((user_password + salt).encode('utf-8')).hexdigest()
