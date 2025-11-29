from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Favorite(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # чтобы один и тот же товар нельзя было добавить дважды
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uix_user_product"),
    )

    product = relationship("Product")
