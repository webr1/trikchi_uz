from pydantic import BaseModel
from typing import List, Optional


# ======================================================
# ORDER ITEM (RESPONSE)
# ======================================================
class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    price: float
    quantity: int

    model_config = {
        "from_attributes": True
    }


# ======================================================
# ORDER (RESPONSE)
# ======================================================
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    items: List[OrderItemResponse] = []

    model_config = {
        "from_attributes": True
    }


# ======================================================
# ORDER ITEM (CREATE)
# ======================================================
class OrderItemCreate(BaseModel):
    product_id: int
    price: float
    quantity: int


# ======================================================
# ORDER (CREATE)
# ======================================================
class OrderCreateSchema(BaseModel):
    items: List[OrderItemCreate]


# ======================================================
# ORDER ITEM (UPDATE)
# ======================================================
class OrderItemUpdateSchema(BaseModel):
    product_id: Optional[int] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


# ======================================================
# ORDER (UPDATE)
# ======================================================
class OrderUpdateSchema(BaseModel):
    status: Optional[str] = None
    total_price: Optional[float] = None
    items: Optional[List[OrderItemUpdateSchema]] = None

    model_config = {
        "from_attributes": True
    }
