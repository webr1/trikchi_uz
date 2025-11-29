from sqlalchemy.orm import Session
from backend.app.schemas.category_schemas import CategoryResponse, CategoryCreate,CategoryUpdate
from backend.app.repositories.category_repository import CategoryRespository
from fastapi import HTTPException, status
from backend.app.core.redis_client import redis_client
import json
from typing import List


class CategoryServices:
    def __init__(self, db: Session):
        self.repository = CategoryRespository(db)
        self.cache_all = "categories:all"

    def get_all_category(self) -> List[dict]:
        cached = redis_client.get(self.cache_all)
        if cached:
            return json.loads(cached)

        categories = self.repository.get_all()

        result = [
            CategoryResponse.model_validate(cat).model_dump()
            for cat in categories
        ]

        redis_client.set(self.cache_all, json.dumps(result), ex=60)

        return result

    def get_category_by_id(self, category_id: int) -> dict:
        cache_key = f"category:{category_id}"

        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        category = self.repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )

        result = CategoryResponse.model_validate(category).model_dump()

        redis_client.set(cache_key, json.dumps(result), ex=120)

        return result

    def get_category_by_slug(self, category_slug: str) -> dict:
        cache_key = f"category_slug:{category_slug}"

        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        category = self.repository.get_by_slug(category_slug)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with slug '{category_slug}' not found"
            )

        result = CategoryResponse.model_validate(category).model_dump()

        redis_client.set(cache_key, json.dumps(result), ex=120)

        return result


    def create_category(self, category_data: CategoryCreate) -> dict:
        category = self.repository.create(category_data)

        redis_client.delete(self.cache_all)
        redis_client.delete(f"category:{category.id}")

        return CategoryResponse.model_validate(category).model_dump()
    
    def update_category(self, category_id: int, data: CategoryUpdate) -> dict:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(404, "Category not found")

        # Обновление полей
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(category, key, value)

        # Сохранить
        self.repository.db.commit()
        self.repository.db.refresh(category)

        # Инвалидация кешей
        redis_client.delete(self.cache_all)
        redis_client.delete(f"category:{category_id}")
        redis_client.delete(f"category_slug:{category.slug}")

        return CategoryResponse.model_validate(category).model_dump()

    def delete_category(self, category_id: int) -> dict:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(404, "Category not found")

        self.repository.db.delete(category)
        self.repository.db.commit()

        # Инвалидация кешей
        redis_client.delete(self.cache_all)
        redis_client.delete(f"category:{category_id}")
        redis_client.delete(f"category_slug:{category.slug}")

        return {"message": "Category deleted successfully"}
