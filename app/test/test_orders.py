from app.test.utils import create_test_user
def test_get_me(client):

    user = create_test_user()

    print("USER:", user.username, user.email)

    login = client.post(
        "/auth/login",
        data={
            "username": "test@test.com",
            "password": "12345678"
        }
    )

    print("LOGIN:", login.json())

    assert login.status_code == 200