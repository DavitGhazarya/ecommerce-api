from fastapi import FastAPI
import app.cloudinary_config
from app.config import settings
from app.routers import auth
from app.routers import products
from app.routers import cart


from app.routers import orders
from app.routers import websocket
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging import log_requests

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(auth.router)

app.include_router(websocket.router)

app.include_router(
    products.router
)
app.include_router(
    cart.router
)
app.include_router(
    orders.router
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)
@app.get("/")
def root():
    return {"message": f"{settings.PROJECT_NAME} is running"}
