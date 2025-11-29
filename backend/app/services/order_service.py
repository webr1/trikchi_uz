from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.app.repositories.order_repository import OrderRepository
from backend.app.schemas.order_schemas import (
    OrderCreateSchema,
    OrderResponse
)


class OrderService:
    def __init__(self, db: Session):
        self.repo = OrderRepository(db)

    # ------------------------------------------------------
    # CREATE ORDER
    # ------------------------------------------------------
    def create_order(self, user_id: int, data: OrderCreateSchema):
        total_price = sum(item.price * item.quantity for item in data.items)

        order = self.repo.create_order(
            user_id=user_id,
            total_price=total_price
        )

        for item in data.items:
            self.repo.add_order_item(
                order_id=order.id,
                product_id=item.product_id,
                price=item.price,
                qty=item.quantity
            )

        # reload with items
        order = self.repo.get_order(order.id)

        return OrderResponse.from_orm(order)

    # ------------------------------------------------------
    # GET ORDER BY ID
    # ------------------------------------------------------
    def get_order(self, order_id: int, user_id: int):
        order = self.repo.get_order(order_id)

        if not order:
            raise HTTPException(404, "Order not found")

        if order.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        return OrderResponse.from_orm(order)

    # ------------------------------------------------------
    # GET ALL USER ORDERS
    # ------------------------------------------------------
    def get_user_orders(self, user_id: int):
        orders = self.repo.get_user_orders(user_id)
        return [OrderResponse.from_orm(order) for order in orders]

    # ------------------------------------------------------
    # UPDATE ORDER STATUS
    # ------------------------------------------------------
    def set_status(self, order_id: int, status: str, user_id: int):
        order = self.repo.get_order(order_id)

        if not order:
            raise HTTPException(404, "Order not found")

        if order.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        updated = self.repo.set_status(order_id, status)

        return OrderResponse.from_orm(updated)
