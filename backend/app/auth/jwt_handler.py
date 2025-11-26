import jwt,time
from datetime import datetime, timedelta
from backend.app.config import settings
from fastapi import HTTPException

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS



def create_access_token(user_id:int) -> str:
    expires = int((datetime.utcnow()+timedelta(minutes=ACCESS_EXPIRE_MINUTES)).timestamp())

    payload = {
        "sub":str(user_id),
        "exp":expires
    }

    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def create_refresh_token(user_id:int) -> str: 
    expires = int((datetime.utcnow()+timedelta(days=REFRESH_EXPIRE_DAYS)).timestamp())

    payload = {
        "sub":str(user_id),
        "exp":expires
    }

    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def decode_token(token:str) -> str:

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(401,"Invalid token")
