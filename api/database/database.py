"""
database.py
-----------

This module is responsible for setting up the database engine and
session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import DATABASE_URL


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Provides a SQLAlchemy database session and ensures it is properly closed
    after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
