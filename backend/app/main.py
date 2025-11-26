from fastapi import FastAPI
from backend.app.routers.registeration_router import router as user_register
import uvicorn
from backend.app.database import Base,engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user_register)




