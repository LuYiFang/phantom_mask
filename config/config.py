"""
config.py
---------

This module contains configuration settings for the application.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")
root_path = Path(os.path.dirname(__file__)).parent

if ENV == "development":
    load_dotenv(dotenv_path=root_path / ".env")
elif ENV == "testing":
    load_dotenv(dotenv_path=root_path / ".env.testing")
elif ENV == "production":
    load_dotenv(dotenv_path=root_path / ".env.prod")
else:
    raise ValueError(f"Unknown environment: {ENV}")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_TEST_DB = os.getenv("POSTGRES_TEST_DB")

DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
TEST_DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                     f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_TEST_DB}")
