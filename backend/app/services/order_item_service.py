from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..repositories.order_item_repository import OrderItemRepository
from ..repositories.order_repository import OrderRepository
from ..schemas.order_schemas import (
    OrderItemCreate,OrderItemResponse

)


class OrderItemService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderItemRepository(db)
        self.order_repo = OrderRepository(db)

    # -----------------------------------------------------
    # CHECK PERMISSION (общая функция)
    # -----------------------------------------------------
    def _check_permission(self, item):
        order = self.order_repo.get_order(item.order_id)
        return order

    # -----------------------------------------------------
    # CREATE ITEM
    # -----------------------------------------------------
    def create_item(self, order_id: int, data: OrderItemCreate, user_id: int):
        # проверяем, что заказ принадлежит пользователю
        order = self.order_repo.get_order(order_id)
        if not order:
            raise HTTPException(404, "Order not found")

        if order.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        # создаём айтем
        item = self.repo.create_item(
            order_id=order_id,
            product_id=data.product_id,
            price=data.price,
            qty=data.quantity
        )

        return OrderItemResponse.model_validate(item).model_dump()

    # -----------------------------------------------------
    # GET ITEM BY ID
    # -----------------------------------------------------
    def get_item(self, item_id: int, user_id: int):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(404, "Order item not found")

        order = self._check_permission(item)
        if order.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        return OrderItemResponse.model_validate(item).model_dump()

    # -----------------------------------------------------
    # GET ITEMS BY ORDER ID
    # -----------------------------------------------------
    def get_items_by_order(self, order_id: int, user_id: int):
        order = self.order_repo.get_order(order_id)
        if not order:
            raise HTTPException(404, "Order not found")

        if order.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        items = self.repo.get_by_order(order_id)

        return [OrderItemResponse.model_validate(i).model_dump() for i in items]

    # -----------------------------------------------------
    # UPDATE ITEM
    # -----------------------------------------------------
    def update_item(self, item_id: int, data: dict, user_id: int):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(404, "Order item not found")

        order = self._check_permission(item)
        if order.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        updated = self.repo.update_item(item, data)

        return OrderItemResponse.model_validate(updated).model_dump()

    # -----------------------------------------------------
    # DELETE ITEM
    # -----------------------------------------------------
    def delete_item(self, item_id: int, user_id: int):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(404, "Order item not found")

        order = self._check_permission(item)
        if order.user_id != user_id:
            raise HTTPException(403, "Forbidden")

        self.repo.delete_item(item)

        return {"message": "Order item removed"}
