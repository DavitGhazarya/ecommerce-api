from fastapi import FastAPI

from app.config import settings
from app.routers import auth
from app.routers import products
from app.routers import cart


from app.routers import orders


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(auth.router)



app.include_router(
    products.router
)
app.include_router(
    cart.router
)
app.include_router(
    orders.router
)
@app.get("/")
def root():
    return {"message": f"{settings.PROJECT_NAME} is running"}
