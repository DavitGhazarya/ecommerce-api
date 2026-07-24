from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user

from app.schemas.cart import (
    CartItemCreate,
    CartResponse
)

from app.services.cart_service import (
    add_item,
    get_cart,
    remove_item
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)



@router.post(
    "/items",
    response_model=CartResponse
)
def add_to_cart(
    data: CartItemCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return add_item(
        db,
        user.id,
        data.product_id,
        data.quantity
    )



@router.get(
    "",
    response_model=CartResponse
)
def read_cart(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return get_cart(
        db,
        user.id
    )



@router.delete(
    "/items/{id}",
    response_model=CartResponse
)
def delete_item(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return remove_item(
        db,
        user.id,
        id
    )