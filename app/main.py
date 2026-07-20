from fastapi import FastAPI

from app.config import settings
from app.routers import auth

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": f"{settings.PROJECT_NAME} is running"}
