from sqlalchemy import Column,Integer,String,Boolean,Text,Float,ForeignKey,DateTime
from backend.app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship



class Product(Base):
    __tablename__= "products"

    id = Column(Integer,primary_key=True,nullable=False,index=True)
    name = Column(String(150),nullable=False,index=True)
    slug = Column(String(150),nullable=False,index=True)
    description = Column(Text)
    price  = Column(Integer,nullable=False)
    category_id = Column(Integer,ForeignKey("categories.id"),nullable=False)
    image_url = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow)

    category = relationship("Category",back_populates="products")
    images = relationship("ProductImage",back_populates="product",cascade="all, delete")

    def __repr__(self):
        return f" name - {self.name} | price - {self.price}"
    

class ProductImage(Base):
    __tablename__="product_images"

    id = Column(Integer,primary_key=True, nullable=False,index=True)
    url = Column(String,nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product",back_populates="images")

    

