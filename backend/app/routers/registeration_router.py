from fastapi import APIRouter , HTTPException, Response,Cookie
from backend.app.models.users import User
from backend.app.schemas.users_schemas import UserRegister, UserResponse ,UserLogin
from backend.app.auth.utils import hash_password, check_password
from sqlalchemy.orm import Session
from backend.app.database import Depends_db
from backend.app.auth.jwt_handler import create_access_token,create_refresh_token,decode_token
from backend.app.config import settings
from urllib.parse import urlencode
from backend.app.models.users import User, SocialAccount
import httpx


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



""" Линк для перехода в Google """
@router.get("/google/login")
def google_login():
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    print("REAL REDIRECT_URI =", settings.GOOGLE_REDIRECT_URI)

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "email profile",
        "access_type": "offline",
        "prompt": "consent"
    }

    return {
        "auth_url": f"{google_auth_url}?{urlencode(params)}"
    }


@router.get("/google/callback")
async def google_callback(code: str, response: Response, db: Session = Depends_db):

    # 1. Получаем access_token от Google
    token_url = "https://oauth2.googleapis.com/token"
    


    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET_KEY,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, data=data)

    token_json = token_res.json()
    google_access_token = token_json.get("access_token")
    google_refresh_token = token_json.get("refresh_token")

    if not google_access_token:
        print("GOOGLE TOKEN ERROR:", token_json)
        raise HTTPException(400, "Failed to authenticate with Google")

    # 2. Получаем userinfo
    async with httpx.AsyncClient() as client:
        info_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {google_access_token}"}
        )

    info = info_res.json()

    google_user_id = info.get("id")
    email = info.get("email")
    name = info.get("name")
    avatar = info.get("picture")

    if not email:
        raise HTTPException(400, "Google did not return an email")

    # 3. Проверяем SocialAccount
    social = (
        db.query(SocialAccount)
        .filter(SocialAccount.provider == "google")
        .filter(SocialAccount.provider_user_id == google_user_id)
        .first()
    )

    if social:
        # Существует social → берём user
        user = social.user
    else:
        # Social нет → ищем user по email
        user = db.query(User).filter(User.email == email).first()

        if not user:
            # Создаём нового пользователя
            user = User(
                name=name,
                email=email,
                avatar_url=avatar,
                password_hash="",
                role="customer",
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Привязываем Google аккаунт
        new_social = SocialAccount(
            user_id=user.id,
            provider="google",
            provider_user_id=google_user_id,
            email=email,
            access_token=google_access_token,
            refresh_token=google_refresh_token
        )

        db.add(new_social)
        db.commit()
        db.refresh(new_social)

    # 4. Создаём JWT токены
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        samesite="lax",
        path="/",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return {
        "access_token": access,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "avatar_url": user.avatar_url
    }
