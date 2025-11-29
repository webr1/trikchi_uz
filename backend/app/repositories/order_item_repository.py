from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from backend.app.models.cart_cartitem import OrderItem


class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------
    # GET ITEM BY ID
    # ---------------------------------------------------
    def get_by_id(self, item_id: int) -> Optional[OrderItem]:
        return (
            self.db.query(OrderItem)
            .options(
                joinedload(OrderItem.product)  # если хочешь брать продукт
            )
            .filter(OrderItem.id == item_id)
            .first()
        )

    # ---------------------------------------------------
    # GET ALL ITEMS FOR ORDER
    # ---------------------------------------------------
    def get_by_order(self, order_id: int) -> List[OrderItem]:
        return (
            self.db.query(OrderItem)
            .options(joinedload(OrderItem.product))
            .filter(OrderItem.order_id == order_id)
            .all()
        )

    # ---------------------------------------------------
    # CREATE ITEM
    # ---------------------------------------------------
    def create_item(self, order_id: int, product_id: int, price: float, qty: int) -> OrderItem:
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            price=price,
            quantity=qty
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # ---------------------------------------------------
    # UPDATE ITEM
    # ---------------------------------------------------
    def update_item(self, item: OrderItem, data: dict) -> OrderItem:
        for key, value in data.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    # ---------------------------------------------------
    # DELETE ITEM
    # ---------------------------------------------------
    def delete_item(self, item: OrderItem):
        self.db.delete(item)
        self.db.commit()
