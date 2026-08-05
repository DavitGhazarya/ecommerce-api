from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    ForeignKey,
    Enum
)

from app.database import Base

import enum


class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    completed = "completed"



class Order(Base):

    __tablename__ = "orders"


    id = Column(
        Integer,
        primary_key=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )


    total_price = Column(
        Numeric(10, 2),
        default=0
    )


    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.pending
    )



class OrderItem(Base):

    __tablename__ = "order_items"


    id = Column(
        Integer,
        primary_key=True
    )


    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )


    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )


    quantity = Column(
        Integer
    )


    price = Column(
        Numeric(10, 2)
    )