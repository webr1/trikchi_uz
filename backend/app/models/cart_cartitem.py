from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    total_price = Column(Integer)
    status = Column(String, default="pending")  # pending / paid / canceled

    items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer)
    price = Column(Integer)
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
