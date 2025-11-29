from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from backend.app.models.cart_cartitem import Order, OrderItem


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------
    # CREATE ORDER
    # ---------------------------------------------------
    def create_order(self, user_id: int, total_price: float) -> Order:
        order = Order(
            user_id=user_id,
            total_price=total_price,
            status="pending"
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    # ---------------------------------------------------
    # ADD ORDER ITEM
    # ---------------------------------------------------
    def add_order_item(self, order_id: int, product_id: int, price: float, qty: int) -> OrderItem:
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
    # GET ORDER WITH ITEMS
    # ---------------------------------------------------
    def get_order(self, order_id: int) -> Optional[Order]:
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.items)  # items подгружаются автоматически
            )
            .filter(Order.id == order_id)
            .first()
        )

    # ---------------------------------------------------
    # GET ALL ORDERS FOR USER
    # ---------------------------------------------------
    def get_user_orders(self, user_id: int) -> List[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.user_id == user_id)
            .all()
        )

    # ---------------------------------------------------
    # UPDATE ORDER STATUS
    # ---------------------------------------------------
    def set_status(self, order_id: int, status: str) -> Optional[Order]:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None

        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order

    # ---------------------------------------------------
    # GET ORDER ITEM
    # ---------------------------------------------------
    def get_item(self, item_id: int) -> Optional[OrderItem]:
        return self.db.query(OrderItem).filter(OrderItem.id == item_id).first()

    # ---------------------------------------------------
    # GET ITEMS BY ORDER
    # ---------------------------------------------------
    def get_items_by_order(self, order_id: int) -> List[OrderItem]:
        return (
            self.db.query(OrderItem)
            .filter(OrderItem.order_id == order_id)
            .all()
        )

    # ---------------------------------------------------
    # UPDATE ORDER ITEM
    # ---------------------------------------------------
    def update_item(self, item: OrderItem, data: dict) -> OrderItem:
        for key, value in data.items():
            setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    # ---------------------------------------------------
    # DELETE ORDER ITEM
    # ---------------------------------------------------
    def delete_item(self, item: OrderItem):
        self.db.delete(item)
        self.db.commit()
