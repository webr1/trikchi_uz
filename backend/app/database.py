from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from fastapi import Depends

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread":False}
)


SessionLocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Depends_db = Depends(get_db)


