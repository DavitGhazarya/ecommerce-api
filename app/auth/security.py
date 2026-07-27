from datetime import datetime, timedelta, timezone
import secrets

from jose import jwt
from passlib.context import CryptContext

from app.config import settings


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
import bcrypt
print(bcrypt.__version__)

def hash_password(password: str):
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password too long")
    print("PASSWORD:", repr(password))
    print("LENGTH:", len(password))
    print("BYTES:", len(password.encode("utf-8")))
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_context.verify(
        password,
        hashed_password
    )


def create_access_token(subject: str):
    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return jwt.encode(
        {
            "sub": subject,
            "exp": expire
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def generate_token():
    return secrets.token_urlsafe(32)