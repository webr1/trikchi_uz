from fastapi import APIRouter , HTTPException, Response,Cookie
from backend.app.models.users import User
from backend.app.schemas.users_schemas import UserRegister, UserResponse ,UserLogin
from backend.app.auth.utils import hash_password, check_password
from sqlalchemy.orm import Session
from backend.app.database import Depends_db
from backend.app.auth.jwt_handler import ALGORITHM, SECRET_KEY, create_access_token,create_refresh_token,decode_token
from backend.app.config import settings
import jwt, time


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
""" Registration проста регисрация """
@router.post("/register",response_model=UserResponse)
def register(user_data:UserRegister,db:Session = Depends_db):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Этот email уже используется")
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password_hash = hash_password(user_data.password),
        role = "customer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
        


""" Login с помощью email, password """
@router.post("/login")
def login(data:UserLogin,response:Response,db:Session=Depends_db):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(404,"User NOT FOUND")

    if not check_password(data.password,user.password_hash):
        raise HTTPException(400,"Invalid Password")
    
    access = create_access_token(user.id)
    refresh =create_refresh_token(user.id)

    response.set_cookie(
        key='refresh_token',
        value=refresh,
        httponly=True,
        samesite="lax",
        path="/",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    return {
        "access_token":access,
        "tyoken_type":'bearer',
        "user_id":user.id
    }


@router.post("/logout")
def logout(response:Response):
    response.delete_cookie(
        key='refresh_token',
        httponly=True,
        samesite="lax",
    )
    return {
        "message":"You loggrd out successfully"
    }


 
"""  Cоздание Access Token с помощью refresh  """
@router.post("/refresh_token")
def refresh(response: Response, refresh_token: str = Cookie(None)):
    print("===> COOKIE FROM CLIENT:", refresh_token)
    
    if refresh_token is None:
        raise HTTPException(401, "Missing refresh token")

    decoded = decode_token(refresh_token)
    if not decoded:
        raise HTTPException(401, "Invalid refresh token")
    
    user_id = decoded["sub"]
    new_access = create_access_token(user_id)

    return {
        "access_token": new_access,
        "token_type": "bearer",
        "user_id": user_id
    }

