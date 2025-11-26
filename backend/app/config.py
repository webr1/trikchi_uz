from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "TRIKCHI_UZ"
    debug: bool = True
    database_url: str = "sqlite:///./trikchi_data.db"
    cors_origins: list = [
        # Порты для фронтенда
        ]
    #Для статических файлов
    static_dir: str = "backend/app/static"
    image_dir: str = "backend/app/static/image"

    # Для хеширование пароли
    SECRET_KEY: str = 'ibdwqyabcqywcwuibiWSBIasgddYEYEBWOFJBVEQO7BIPSbcybbyby3ub2ib2ibfedbcs7cb'
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30 


    class Config:
        env_file  = ".env"


settings = Settings()