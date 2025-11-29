from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.order_item_service import OrderItemService
from backend.app.schemas.order_schemas import (
    OrderItemCreate,
    OrderItemResponse
)
from backend.app.auth.permissions import get_current_user

router = APIRouter(
    prefix="/order-items",
    tags=["Order Items"]
)


# -----------------------------------------------------------
# CREATE ORDER ITEM
# -----------------------------------------------------------
@router.post("/{order_id}", response_model=OrderItemResponse)
def create_order_item(
    order_id: int,
    data: OrderItemCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    service = OrderItemService(db)
    return service.create_item(order_id, data, user_id=user["id"])


# -----------------------------------------------------------
# GET ONE ORDER ITEM
# -----------------------------------------------------------
@router.get("/item/{item_id}", response_model=OrderItemResponse)
def get_order_item(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    service = OrderItemService(db)
    return service.get_item(item_id, user_id=user["id"])


# -----------------------------------------------------------
# GET ALL ITEMS BY ORDER ID
# -----------------------------------------------------------
@router.get("/order/{order_id}", response_model=list[OrderItemResponse])
def get_items_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    service = OrderItemService(db)
    return service.get_items_by_order(order_id, user_id=user["id"])


# -----------------------------------------------------------
# UPDATE ORDER ITEM
# -----------------------------------------------------------
@router.put("/item/{item_id}", response_model=OrderItemResponse)
def update_order_item(
    item_id: int,
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    service = OrderItemService(db)
    return service.update_item(item_id, data, user_id=user["id"])


# -----------------------------------------------------------
# DELETE ORDER ITEM
# -----------------------------------------------------------
@router.delete("/item/{item_id}")
def delete_order_item(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    service = OrderItemService(db)
    return service.delete_item(item_id, user_id=user["id"])
