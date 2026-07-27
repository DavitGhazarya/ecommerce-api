from app.auth.security import hash_password
from app.database import SessionLocal
from app.models.user import User


def create_test_user():

    db = SessionLocal()

    user = User(
        username="test@test.com",
        email="test@test.com",
        hashed_password=hash_password("12345678"),
        is_verified=True
    )

    db.add(user)
    db.commit()
    db.close()



def test_register_success(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "12345678"
        }
    )

    assert response.status_code == 201



def test_login_success(client):

    create_test_user()

    response = client.post(
        "/auth/login",
        data={
            "username": "test@test.com",
            "password": "12345678"
        }
    )

    print(response.json())

    assert response.status_code == 200
    assert "access_token" in response.json()



def test_get_me(client):

    create_test_user()

    login = client.post(
        "/auth/login",
        data={
            "username": "test@test.com",
            "password": "12345678"
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200