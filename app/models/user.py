import enum
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Boolean,
    func
)

from app.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    SELLER = "seller"
    ADMIN = "admin"



class User(Base):
    __tablename__ = "users"

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )


    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )


    hashed_password = Column(
        String(255),
        nullable=False
    )


    role = Column(
        Enum(
            UserRole,
            name="user_role",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        nullable=False,
        default=UserRole.USER
    )


    is_verified = Column(
        Boolean,
        nullable=False,
        default=False
    )


    verification_token = Column(
        String(255),
        nullable=True
    )


    verification_token_expire = Column(
        DateTime(timezone=True),
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    reset_password_token = Column(
        String,
        nullable=True
    )

    reset_password_token_expire = Column(
        DateTime,
        nullable=True
    )

    products = relationship(
        "Product",
        back_populates="seller"
    )