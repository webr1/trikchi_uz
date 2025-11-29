from pydantic import BaseModel
from typing import List


# ----------- CartItem (для ответа API) -----------
class CartItemSchema(BaseModel):
    product_id: int
    title: str
    price: int
    quantity: int
    subtotal: int

    class Config:
        orm_mode = True


# ----------- Request схема для изменения количества -----------
class CartQuantityUpdate(BaseModel):
    qty: int


# ----------- Полная корзина (ответ API) -----------
class CartSchema(BaseModel):
    items: List[CartItemSchema]
    total: int

    class Config:
        orm_mode = True
