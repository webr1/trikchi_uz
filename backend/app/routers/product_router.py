from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import Depends_db, get_db
from ..services.product_images_service import ProductServices
from ..services.product_services import ProductService
from backend.app.schemas.product_shcemas import ProductCreate, ProductResponse, ProductUpdate


router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)


@router.get("/all", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_id(product_id)

@router.get("/slug/{slug}", response_model=ProductResponse)
def get_product_slug(slug: str, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_slug(slug)

@router.post("/create", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.create_product(product_in)

@router.put("/update/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.update_product(product_id, data)

@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.delete_product(product_id)

@router.post("/{product_id}")
async def upload_images(
    product_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends_db
):
    service = ProductServices(db)
    return await service.add_images(product_id, files)