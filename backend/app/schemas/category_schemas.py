from pydantic import BaseModel,Field



class CategoryBase(BaseModel):
    name: str = Field(..., min_length=5,max_length=150,description="Введити название")
    slug: str = Field(..., min_length=5,max_length=100,description="URL-frendly category name")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class CategoryResponse(CategoryBase):
    id: int = Field(...,deprecated="Уникальный иденификатор Category")


    class Config:
        from_attributes = True