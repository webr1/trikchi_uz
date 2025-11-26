from sqlalchemy import Boolean,Column,String,Integer,Text,DateTime,ForeignKey
from backend.app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__="users"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(100),index=True)
    email = Column(String(150),unique=True,index=True)
    phone = Column(String(13),unique=True,index=True)
    password_hash = Column(String(225),nullable=False)
    role = Column(String(20),default="customer",index=True)
    avatar_url = Column(Text)
    is_superuser = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow)

    social_accounts = relationship("SocialAccount",back_populates="user")



class SocialAccount(Base):
    __tablename__="social_accounts"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    provider = Column(String(50))
    provider_user_id = Column(String(150))
    email = Column(String(150))
    access_token = Column(Text)
    refresh_token = Column(Text)
    created_at = Column(DateTime,default=datetime.utcnow)

    user = relationship("User",back_populates="social_accounts")