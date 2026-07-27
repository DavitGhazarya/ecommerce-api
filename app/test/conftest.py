import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine


@pytest.fixture
def client():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    return TestClient(app)