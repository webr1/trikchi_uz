from fastapi import FastAPI
from backend.app.routers.registeration_router import router as user_router
from .routers.category_router import router as catrgory_router
from .routers.product_router import router as product_router
from .routers.wishlist_router import router as wishlist_router
from backend.app.database import Base,engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user_router)
app.include_router(catrgory_router)
app.include_router(product_router)
app.include_router(wishlist_router)



