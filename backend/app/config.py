from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
    app_name: str = "TRIKCHI_UZ"
    debug: bool
    database_url: str 
    cors_origins: list = [
        # Порты для фронтенда
        ]
    #Для статических файлов
    static_dir: str = "backend/app/static"
    image_dir: str = "backend/app/static/image"

    # Для хеширование пароли
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30 

    #Для хронения секретных ключев
    GOOGLE_CLIENT_ID: str 
    GOOGLE_CLIENT_SECRET_KEY: str 
    GOOGLE_REDIRECT_URI: str 




    class Config:
        env_file  = ".env"


settings = Settings()