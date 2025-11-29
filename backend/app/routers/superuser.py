from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db   
from ..auth.permissions import admin_required   # твоя проверка: только админы
from ..schemas.users_schemas import UserRegister, UserUpdate, UserResponse
from ..auth.permissions import SuperUserService


router = APIRouter(
    prefix="/superusers",
    tags=["Superusers"]
)


# ----------------------------------------
# CREATE SUPERUSER
# ----------------------------------------
@router.post("/create", response_model=UserResponse)
def create_superuser(
    data: UserRegister,
    db: Session = Depends(get_db),
    admin = Depends(admin_required),   # только суперюзер может создать суперюзера
):
    return SuperUserService.create_superuser(data, db)


# ----------------------------------------
# UPDATE SUPERUSER
# ----------------------------------------
@router.patch("/{user_id}/update", response_model=UserResponse)
def update_superuser(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    admin = Depends(admin_required),
):
    return SuperUserService.update_superuser(user_id, data, db)


# ----------------------------------------
# DELETE SUPERUSER
# ----------------------------------------
@router.delete("/{user_id}/delete")
def delete_superuser(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required),  # нельзя удалить себя
):
    return SuperUserService.delete_superuser(user_id, admin, db)


# ----------------------------------------
# GET ONE SUPERUSER
# ----------------------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_superuser(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required),
):
    return SuperUserService.get_superuser(user_id, db)


# ----------------------------------------
# GET ALL SUPERUSERS
# ----------------------------------------
@router.get("/", response_model=list[UserResponse])
def get_superusers(
    db: Session = Depends(get_db),
    admin = Depends(admin_required),
):
    return SuperUserService.get_superusers(db)
