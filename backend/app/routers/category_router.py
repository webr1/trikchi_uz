from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import Depends_db
from backend.app.services.category_services import CategoryServices
from backend.app.schemas.category_schemas import CategoryResponse, CategoryCreate, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/all",response_model=List[CategoryResponse],status_code=status.HTTP_200_OK)
def get_categories(db:Session = Depends_db):
    service = CategoryServices(db)
    return service.get_all_category()

@router.post("/create",response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
def create_category(category_in:CategoryCreate,db:Session = Depends_db):
    service = CategoryServices(db)
    return service.create_category(category_in)

@router.get("/{category_id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
def get_category(category_id:int,db:Session = Depends_db):
    service = CategoryServices(db)
    return service.get_category_by_id(category_id)

@router.get("/{category_slug}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category(category_slug: str, db: Session = Depends_db):
    service = CategoryServices(db)
    return service.get_category_by_slug(category_slug)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends_db):
    service = CategoryServices(db)
    return service.update_category(category_id, data)

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends_db):
    service = CategoryServices(db)
    return service.delete_category(category_id)
