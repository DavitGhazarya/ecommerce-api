from app.auth.security import hash_password
from app.database import SessionLocal
from app.models.user import User


def create_test_user():

    db = SessionLocal()

    user = User(
        username="seller@test.com",
        email="seller@test.com",
        hashed_password=hash_password("12345678"),
        is_verified=True,
        role="seller"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    db.close()

    return user



def login(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "seller@test.com",
            "password": "12345678"
        }
    )

    return response.json()["access_token"]



def test_create_product(client):

    create_test_user()

    token = login(client)

    response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "description": "Test description",
            "price": 100,
            "stock": 10
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert response.status_code == 201



def test_get_products(client):

    response = client.get(
        "/products"
    )

    assert response.status_code == 200