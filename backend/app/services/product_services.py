import json
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repositories.prodcut_repository import ProductRepository
from backend.app.schemas.product_shcemas import ProductCreate, ProductUpdate, ProductResponse
from backend.app.core.redis_client import redis_client


class ProductService:
    CACHE_ALL = "products:all"
    CACHE_PRODUCT = "product:{}"
    CACHE_SLUG = "product_slug:{}"

    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    # -------------------------------------
    # GET ALL
    # -------------------------------------
    def get_all_products(self):
        cached = redis_client.get(self.CACHE_ALL)
        if cached:
            return json.loads(cached)

        products = self.repo.get_all()
        result = [ProductResponse.model_validate(p).model_dump() for p in products]

        redis_client.set(self.CACHE_ALL, json.dumps(result, default=str), ex=60)
        return result

    # -------------------------------------
    # GET BY ID
    # -------------------------------------
    def get_product_by_id(self, product_id: int):
        key = self.CACHE_PRODUCT.format(product_id)

        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)

        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        result = ProductResponse.model_validate(product).model_dump()
        redis_client.set(key, json.dumps(result, default=str), ex=120)

        return result

    # -------------------------------------
    # GET BY SLUG
    # -------------------------------------
    def get_product_by_slug(self, slug: str):
        key = self.CACHE_SLUG.format(slug)

        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)

        product = self.repo.get_by_slug(slug)
        if not product:
            raise HTTPException(404, "Product not found")

        result = ProductResponse.model_validate(product).model_dump()
        redis_client.set(key, json.dumps(result, default=str), ex=120)

        return result

    # -------------------------------------
    # CREATE
    # -------------------------------------
    def create_product(self, data: ProductCreate):
        product = self.repo.create(data)

        redis_client.delete(self.CACHE_ALL)
        redis_client.delete(self.CACHE_PRODUCT.format(product.id))
        redis_client.delete(self.CACHE_SLUG.format(product.slug))

        return ProductResponse.model_validate(product).model_dump()

    # -------------------------------------
    # UPDATE
    # -------------------------------------
    def update_product(self, product_id: int, data: ProductUpdate):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        self.repo.db.commit()
        self.repo.db.refresh(product)

        redis_client.delete(self.CACHE_ALL)
        redis_client.delete(self.CACHE_PRODUCT.format(product_id))
        redis_client.delete(self.CACHE_SLUG.format(product.slug))

        return ProductResponse.model_validate(product).model_dump()

    # -------------------------------------
    # DELETE
    # -------------------------------------
    def delete_product(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        self.repo.db.delete(product)
        self.repo.db.commit()

        redis_client.delete(self.CACHE_ALL)
        redis_client.delete(self.CACHE_PRODUCT.format(product_id))
        redis_client.delete(self.CACHE_SLUG.format(product.slug))

        return {"message": "Product deleted successfully"}
