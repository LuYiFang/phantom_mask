"""
tools.py
--------

This module contains utility functions for the application.
"""

import json
import logging
from fastapi import HTTPException
from sqlalchemy import text


def exception_handler(func):
    """
    Decorator to handle exceptions for the given function.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.exception('%s', e)
            raise HTTPException(status_code=500, detail=str(e)) from e

    return wrapper


def install_pg_trgm(engine):
    """
    Install the pg_trgm extension if not already installed.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm'"))
        if not result.scalar():
            connection.execute(text("CREATE EXTENSION pg_trgm"))
            connection.commit()


def generate_openapi_json(app):
    """
    Generate the OpenAPI JSON file for the application.
    """
    with open("../openapi.json", "w", encoding="utf-8") as file:
        json.dump(app.openapi(), file)
