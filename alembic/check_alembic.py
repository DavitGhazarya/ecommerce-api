from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://postgres:1234@localhost:5432/ecommerce_db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM alembic_version")
    )

    for row in result:
        print(row)