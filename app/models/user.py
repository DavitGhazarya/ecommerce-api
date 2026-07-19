import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from app.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # для будущей ролевой авторизации
=======
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, name="user_role"), nullable=False, default=UserRole.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
>>>>>>> db8f1c1 (Add JWT authentication and Alembic setup)
