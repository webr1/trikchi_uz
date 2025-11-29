import re
from pydantic import BaseModel,EmailStr,ConfigDict,field_validator
from typing  import Optional,List



""" Общая база: ORM mode включен """
class   ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

""" СХЕМА: Регистрация """
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls,password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Za-z]", password):
            raise ValueError("Password must include letters")
        if not re.search(r"\d", password):
            raise ValueError("Password must include digits")
        return password

""" СХЕМА: Логин """
class UserLogin(BaseModel):
    email: EmailStr
    password: str


""" # СХЕМА: Ответ при возврате User """
class UserResponse(ORMBase):
        id: int
        name: str
        email: Optional[str] = None
        phone: Optional[str] = None
        avatar_url: Optional[str] = None
        role: str
        is_superuser:bool


""" СХЕМА: Социальные аккаунты """
class SocialAccountResponse(ORMBase):
    id:int
    provider: str
    provider_user_id: str
    email: Optional[str] = None
    

""" СХЕМА: Полный профиль (User + Socials) """
class UserFullResponse(UserResponse):
    social_accounts: List[SocialAccountResponse] = []


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, password):
        if password is None:
            return password
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Za-z]", password):
            raise ValueError("Password must include letters")
        if not re.search(r"\d", password):
            raise ValueError("Password must include digits")
        return password
