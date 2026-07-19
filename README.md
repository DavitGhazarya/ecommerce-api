# E-commerce API

1. Create a PostgreSQL database named `ecommerce_db`.
2. Copy `.env.example` to `.env` and set the database password and a new `SECRET_KEY`.
3. In PyCharm, create a virtual environment and run `pip install -r requirements.txt`.
4. Run `alembic upgrade head`, then `uvicorn app.main:app --reload`.

Open `http://127.0.0.1:8000/docs` for Swagger UI.

Authentication: `POST /auth/register`, `POST /auth/login`, and `GET /auth/me`.
