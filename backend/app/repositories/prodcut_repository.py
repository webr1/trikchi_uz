from sqlalchemy.orm import Session,joinedload
from typing import List,Optional
from backend.app.models.product import Product
from backend.app.schemas.product_shcemas import ProductCreate



class ProductRepository:
    def __init__(self,db:Session):
        self.db = db

    def get_all(self) -> List[Product]:
        return self.db.query(Product).options(joinedload(Product.category),joinedload(Product.images)).all()
    
    def get_by_id(self,product_id:int) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category),joinedload(Product.images))
            .filter(Product.id==product_id).first()
        )
    
    def get_by_slug(self,product_slug:str) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category),joinedload(Product.images))
            .filter(Product.slug==product_slug)
            .first()

        )
    def get_by_category(self,product_category:int) -> Optional[Product]:
        return (
            self.db.query(Product).
            options(joinedload(Product.category),joinedload(Product.images))
            .filter(Product.category_id == product_category)
            .first()
        )
    
    def create(self,product_data:ProductCreate) -> Product:

        db_product = Product(**product_data.model_dump())

        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)

        return db_product
    
    def get_multiple_by_ids(self,product_ids:List[int]) -> List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category),joinedload(Product.images))
            .filter(Product.id.in_(product_ids))
            .all()
        )