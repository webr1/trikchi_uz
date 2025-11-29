from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.order_service import OrderService
from backend.app.schemas.order_schemas import (
    OrderCreateSchema,
    OrderResponse
)
from backend.app.auth.permissions import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create", response_model=OrderResponse)
def create_order(
    data: OrderCreateSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    service = OrderService(db)
    return service.create_order(user_id=user["id"], data=data)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    service = OrderService(db)
    return service.get_order(order_id=order_id, user_id=user["id"])


@router.get("/", response_model=list[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    service = OrderService(db)
    return service.get_user_orders(user_id=user["id"])
