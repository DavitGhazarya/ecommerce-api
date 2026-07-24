from fastapi import HTTPException

from app.models.order import Order, OrderItem
from app.models.cart import Cart


def create_order(db, user_id):

    cart = db.query(Cart).filter(
        Cart.user_id == user_id
    ).first()


    if not cart or not cart.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )


    order = Order(
        user_id=user_id,
        total_price=0
    )

    db.add(order)
    db.flush()


    total = 0


    for item in cart.items:

        price = item.product.price

        total += price * item.quantity


        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=price
        )

        db.add(order_item)


    order.total_price = total


    # очистка корзины
    for item in cart.items:
        db.delete(item)


    db.commit()
    db.refresh(order)


    return order



def get_orders(db, user_id):

    return db.query(Order).filter(
        Order.user_id == user_id
    ).all()



def get_order(db, user_id, order_id):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()


    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )


    return order