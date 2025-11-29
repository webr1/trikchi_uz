from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from ..config import settings
from sqlalchemy.orm import Session
from ..database import Depends_db
from ..models.users import User
from ..schemas.users_schemas import UserRegister, UserUpdate
from sqlalchemy.orm import Session
from backend.app.models import User
from .utils import hash_password
from ..schemas.users_schemas import UserRegister, UserUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends_db
):
    try:
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = int(data["sub"])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def admin_required(
    current_user: User = Depends(get_current_user),
    db: Session = Depends_db,
):
    """
    Разрешает доступ только суперюзерам.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admins only")

    return current_user

class SuperUserService:


    @staticmethod
    def create_superuser(data: UserRegister, db: Session):

        total_superusers = (
            db.query(User).filter(User.is_superuser == True).count()
        )
        if total_superusers >= 5:
            raise HTTPException(403, "Too many superusers")

        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(400, "Email already exists")

        superuser = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            is_superuser=True,
        )

        db.add(superuser)
        db.commit()
        db.refresh(superuser)

        return superuser


    @staticmethod
    def update_superuser(user_id: int, data: UserUpdate, db: Session):

        superuser = (
            db.query(User)
            .filter(User.id == user_id, User.is_superuser == True)
            .first()
        )

        if not superuser:
            raise HTTPException(404, "Superuser not found")

        if data.name:
            superuser.name = data.name

        if data.email:
            # проверка на занятость
            exists = db.query(User).filter(
                User.email == data.email,
                User.id != user_id
            ).first()
            if exists:
                raise HTTPException(400, "Email already taken")

            superuser.email = data.email

        if data.phone:
            superuser.phone = data.phone

        if data.avatar_url:
            superuser.avatar_url = data.avatar_url

        if data.password:
            superuser.password = hash_password(data.password)

        db.commit()
        db.refresh(superuser)
        return superuser

    @staticmethod
    def delete_superuser(user_id: int, current_admin: User, db: Session):

        if current_admin.id == user_id:
            raise HTTPException(403, "You cannot delete yourself")

        superuser = (
            db.query(User)
            .filter(User.id == user_id, User.is_superuser == True)
            .first()
        )

        if not superuser:
            raise HTTPException(404, "Superuser not found")

        db.delete(superuser)
        db.commit()

        return {"message": "Superuser deleted successfully"}

    @staticmethod
    def get_superuser(user_id: int, db: Session):
        user = (
            db.query(User)
            .filter(User.id == user_id, User.is_superuser == True)
            .first()
        )

        if not user:
            raise HTTPException(404, "Superuser not found")

        return user


    @staticmethod
    def get_superusers(db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(User)
            .filter(User.is_superuser == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
