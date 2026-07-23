from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate



def create_product(
        db: Session,
        data: ProductCreate,
        seller_id: int
):

    product = Product(
        **data.model_dump(),
        seller_id=seller_id
    )


    db.add(product)

    db.commit()

    db.refresh(product)

    return product


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort: str | None = None
):

    query = (
        db.query(Product)
        .filter(Product.is_active == True)
    )


    # Search
    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )


    # Price filtering
    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )


    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )


    # Sorting
    if sort:

        if sort == "price":
            query = query.order_by(
                Product.price.asc()
            )

        elif sort == "-price":
            query = query.order_by(
                Product.price.desc()
            )


        elif sort == "newest":
            query = query.order_by(
                Product.created_at.desc()
            )

    total = query.count()

    products = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return products, total


def get_product(
        db: Session,
        product_id: int
):

    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )



def delete_product(
        db: Session,
        product: Product
):

    product.is_active = False

    db.commit()
def update_product(
    db: Session,
    product: Product,
    data
):

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            product,
            key,
            value
        )

    db.commit()

    db.refresh(product)

    return product