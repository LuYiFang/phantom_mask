import json
import logging
import os

from fastapi import HTTPException
from sqlalchemy import text

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_TEST_DB = os.getenv("POSTGRES_TEST_DB")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
TEST_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_TEST_DB}"


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.exception(f'{e}')
            raise HTTPException(status_code=500, detail=str(e))

    return wrapper


def install_pg_trgm(engine):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm'"))
        if not result.scalar():
            connection.execute(text("CREATE EXTENSION pg_trgm"))
            connection.commit()


def generate_openapi_json(app):
    with open("openapi.json", "w") as file:
        json.dump(app.openapi(), file)
