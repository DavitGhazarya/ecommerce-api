from fastapi import FastAPI

from app.config import settings
from app.routers import auth
from app.routers import products
app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(auth.router)



app.include_router(
    products.router
)

@app.get("/")
def root():
    return {"message": f"{settings.PROJECT_NAME} is running"}
