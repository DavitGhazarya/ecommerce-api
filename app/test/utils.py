from app.database import SessionLocal
from app.models.user import User
from app.auth.security import hash_password


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
    db.refresh(user)

    db.close()

    return user