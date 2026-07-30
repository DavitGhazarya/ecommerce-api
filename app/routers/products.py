from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from fastapi import status

from app.database import get_db

from app.schemas.product import (
    ProductCreate,
    ProductResponse
)

from app.services.product_service import (
    create_product,
    get_products,
    get_product,
    delete_product
)


from app.auth.dependencies import get_current_user

from app.schemas.product import ProductListResponse
from fastapi import UploadFile, File
from app.services.image_service import upload_image


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

from app.schemas.product import ProductUpdate
from app.services.product_service import (
    update_product
)
@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user.role.value not in ["seller", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    return create_product(
        db,
        data,
        user.id
    )

@router.get(
    "/",
    response_model=ProductListResponse
)
def products(
    page: int = 1,
    limit: int = 10,

    search: str | None = None,

    min_price: float | None = None,

    max_price: float | None = None,

    sort: str | None = None,

    db: Session = Depends(get_db)

):

    skip = (page - 1) * limit


    products, total = get_products(
        db,
        skip,
        limit,
        search,
        min_price,
        max_price,
        sort
    )


    return {
        "items": products,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get(
    "/my",
    response_model=list[ProductResponse]
)
def my_products(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    if user.role.value not in [
        "seller",
        "admin"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )


    from app.models.product import Product


    products = db.query(Product).filter(
        Product.seller_id == user.id
    ).all()


    return products
@router.get(
    "/{id}",
    response_model=ProductResponse
)
def get_one(
    id:int,
    db:Session = Depends(get_db)
):

    product = get_product(
        db,
        id
    )


    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    return product


@router.put(
    "/{id}",
    response_model=ProductResponse
)
def update(
    id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    product = get_product(
        db,
        id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    if product.seller_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )


    return update_product(
        db,
        product,
        data
    )
@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    product = get_product(
        db,
        id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if (
        product.seller_id != user.id
        and user.role.value != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted"
    }

@router.post("/{id}/image")
def upload_product_image(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    product = get_product(db, id)

    if not product:
        raise HTTPException(
            404,
            "Product not found"
        )

    if product.seller_id != user.id:
        raise HTTPException(
            403,
            "Not allowed"
        )


    image_url = upload_image(
        file.file
    )


    product.image_url = image_url

    db.commit()
    db.refresh(product)


    return {
        "image_url": product.image_url
    }