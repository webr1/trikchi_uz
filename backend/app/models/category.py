from sqlalchemy import String,Integer,Column,DateTime
from backend.app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship



class Category(Base):
    __tablename__="categories"

    id = Column(Integer,primary_key=True,nullable=False,index=True)
    name = Column(String(100),nullable=False,index=True)
    slug = Column(String(100),nullable=False,index=True)
    created_at = Column(DateTime,default=datetime.utcnow)

    products = relationship("Product",back_populates="category")

    def __repr__(self):
        return f"name - {self.name}, created - {self.created_at}"
