from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session


from app.database import get_db
from app.auth.dependencies import get_current_user

from app.schemas.order import OrderResponse

from app.services.order_service import (
    create_order,
    get_orders,
    get_order
)



router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)



# POST /orders
@router.post(
    "/",
    response_model=OrderResponse
)
def create(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return create_order(
        db,
        user.id
    )



# GET /orders
@router.get(
    "/",
    response_model=list[OrderResponse]
)
def read_all(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return get_orders(
        db,
        user.id
    )



# GET /orders/{id}
@router.get(
    "/{id}",
    response_model=OrderResponse
)
def read_one(
    id:int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return get_order(
        db,
        user.id,
        id
    )