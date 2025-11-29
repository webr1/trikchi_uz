from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import redis

from backend.app.auth.permissions import get_current_user
from backend.app.config import settings
from backend.app.core import redis_client
from backend.app.database import Depends_db
from backend.app.models.users import User
from ..models.product import Product
from backend.app.models.wishlist import Favorite


router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)

@router.post("/add/{product_id}")
def add_to_wishlist(
    product_id: int,
    db: Session = Depends_db,
    user: User = Depends(get_current_user)
):
    # Проверяем, что товар существует
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    # Redis key
    key = f"wishlist:{user.id}"

    # Добавляем в Redis (Set)
    redis_client.sadd(key, product_id)

    # Добавляем в БД, если нет
    exists = db.query(Favorite).filter(
        Favorite.user_id == user.id,
        Favorite.product_id == product_id
    ).first()

    if not exists:
        item = Favorite(user_id=user.id, product_id=product_id)
        db.add(item)
        db.commit()
        db.refresh(item)

    return {"message": "Added to wishlist"}

@router.get("/")
def get_user_wishlist(
    db: Session = Depends_db,
    user: User = Depends(get_current_user)
):
    key = f"wishlist:{user.id}"

    # Пробуем получить список из Redis
    product_ids = redis_client.smembers(key)

    # Если в Redis пусто — берём из базы и обновляем Redis
    if not product_ids:
        items = db.query(Favorite).filter(Favorite.user_id == user.id).all()
        product_ids = [i.product_id for i in items]

        if product_ids:
            redis_client.sadd(key, *product_ids)

    # Загружаем товары из базы
    if product_ids:
        products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    else:
        products = []

    return products

@router.delete("/remove/{product_id}")
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends_db,
    user: User = Depends(get_current_user)
):
    key = f"wishlist:{user.id}"

    # Удаляем из Redis
    redis_client.srem(key, product_id)

    # Удаляем из базы
    exists = db.query(Favorite).filter(
        Favorite.user_id == user.id,
        Favorite.product_id == product_id
    ).first()

    if exists:
        db.delete(exists)
        db.commit()

    return {"message": "Removed from wishlist"}
