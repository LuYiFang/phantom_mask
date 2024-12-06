import logging

from fastapi import HTTPException


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
