from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
from backend.app.schemas.category_schemas import CategoryResponse


class ProductImageResponse(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(..., min_length=5,max_length=150,description="Введити название")
    slug: str = Field(..., min_length=5,max_length=100,description="URL-frendly PRODUCT name")
    description: Optional[str] = None
    price: float = Field(...,gt=0)
    category_id: int
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    price: float | None = None
    category_id: int | None = None



class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]
    created_at: datetime

    category: Optional[CategoryResponse] = None
    images: list[ProductImageResponse]

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int

    class Config:
        from_attributes = True
