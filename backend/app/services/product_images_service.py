from fastapi import HTTPException
from ..models.product import Product, ProductImage
import uuid
import os

class ProductServices:
    def __init__(self, db):
        self.db = db

    async def add_images(self, product_id: int, files):
        product = self.db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(404, "Product not found")

        saved_images = []

        for file in files:
            ext = file.filename.split(".")[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            filepath = f"backend/app/media/products/{filename}"

            # сохраняем файл
            with open(filepath, "wb") as buffer:
                buffer.write(await file.read())

            # создаём запись в БД
            image = ProductImage(
                url=f"/media/products/{filename}",
                product_id=product_id
            )
            self.db.add(image)
            saved_images.append(image)

        self.db.commit()
        return saved_images
