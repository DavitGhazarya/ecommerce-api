# E-commerce API

FastAPI + PostgreSQL + SQLAlchemy + Alembic + JWT authentication.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your real PostgreSQL password:
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and set `DATABASE_URL` with your real password, and set `SECRET_KEY` to any random string.

3. Create the database in pgAdmin (or via SQL):
   ```sql
   CREATE DATABASE ecommerce_db;
   ```

4. Run the migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Open the API docs:
   ```
   http://127.0.0.1:8000/docs
   ```

## Endpoints

- `POST /auth/register` — register a new user
- `POST /auth/login` — log in, returns a JWT access token
- `GET /auth/me` — get the current logged-in user (requires Bearer token)
