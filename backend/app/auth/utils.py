from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated ="auto")

"""Хеширование пароля (argon2)."""
def hash_password(password:str) -> str:
    return pwd_context.hash(password)


"""Проверка пароля."""
def  check_password(log_password:str,hashed_password:str) -> bool:
    return pwd_context.verify(log_password,hashed_password)


