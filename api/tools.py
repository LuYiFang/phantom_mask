import logging

from fastapi import HTTPException
from sqlalchemy import text


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
