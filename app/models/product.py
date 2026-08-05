from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    func
)

from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):

    __tablename__ = "products"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String(100),
        nullable=False,
        index=True
    )


    description = Column(
        Text,
        nullable=True
    )


    price = Column(
        Numeric(10, 2),
        nullable=False
    )


    stock = Column(
        Integer,
        default=0
    )


    image_url = Column(
        String,
        nullable=True
    )


    is_active = Column(
        Boolean,
        default=True
    )


    seller_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    created_at = Column(
        DateTime,
        server_default=func.now()
    )


    updated_at = Column(
        DateTime,
        onupdate=func.now()
    )


    seller = relationship(
        "User",
        back_populates="products"
    )
    image_url = Column(
        String,
        nullable=True
    )