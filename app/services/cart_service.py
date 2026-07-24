from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product


def get_or_create_cart(
    db: Session,
    user_id: int
):

    cart = (
        db.query(Cart)
        .filter(
            Cart.user_id == user_id
        )
        .first()
    )


    if not cart:
        cart = Cart(
            user_id=user_id
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)


    return cart



def add_item(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int
):

    cart = get_or_create_cart(
        db,
        user_id
    )


    product = (
        db.query(Product)
        .filter(
            Product.id == product_id
        )
        .first()
    )


    if not product:
        return None


    item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
        .first()
    )


    if item:

        item.quantity += quantity

    else:

        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )

        db.add(item)


    db.commit()
    db.refresh(cart)

    return cart



def get_cart(
    db: Session,
    user_id: int
):

    return get_or_create_cart(
        db,
        user_id
    )



def remove_item(
    db: Session,
    user_id: int,
    item_id: int
):

    cart = get_or_create_cart(
        db,
        user_id
    )


    item = (
        db.query(CartItem)
        .filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart.id
        )
        .first()
    )


    if item:

        db.delete(item)
        db.commit()


    return cart