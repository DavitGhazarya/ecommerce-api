from fastapi import FastAPI
import app.cloudinary_config
from app.config import settings
from app.routers import auth
from app.routers import products
from app.routers import cart
from fastapi.staticfiles import StaticFiles


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
        "http://localhost:3000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"


app.mount(
    "/app",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True
    ),
    name="frontend"
)


@app.get("/")
def root():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )
