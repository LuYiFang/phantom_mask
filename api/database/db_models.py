"""
db_models.py
------------

This module defines the SQLAlchemy database models for the application.

Each model represents a table in the database with relationships and attributes
required for the application's functionality.
"""

from sqlalchemy import (Column, Integer, String, ForeignKey, Numeric, Time,
                        DateTime)
from sqlalchemy.orm import relationship

from api.database.database import Base


class Pharmacy(Base):
    """
    Represents a pharmacy.
    """
    __tablename__ = 'pharmacies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    cash_balance = Column(Numeric(10, 2), nullable=False)
    opening_hours = relationship(
        "PharmacyHour",
        back_populates="pharmacy",
        cascade="all, delete-orphan"
    )
    pharmacy_masks = relationship("PharmacyMask", back_populates="pharmacy")
    transactions = relationship("Transaction", back_populates="pharmacy")


class PharmacyHour(Base):
    """
    Represents the operating hours of a pharmacy.
    """
    __tablename__ = 'pharmacy_hours'
    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(Integer, ForeignKey('pharmacies.id'), index=True)
    day_of_week = Column(String(10), nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    pharmacy = relationship("Pharmacy", back_populates="opening_hours")


class Mask(Base):
    """
    Represents a mask.
    """
    __tablename__ = 'masks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    prices = relationship("PharmacyMask", back_populates="mask")
    transactions = relationship("Transaction", back_populates="mask")


class PharmacyMask(Base):
    """
    Represents the price of a mask at a specific pharmacy.
    """
    __tablename__ = 'pharmacy_masks'
    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(Integer, ForeignKey('pharmacies.id'), index=True)
    mask_id = Column(Integer, ForeignKey('masks.id'), index=True)
    price = Column(Numeric(10, 2), nullable=False)
    pharmacy = relationship("Pharmacy", back_populates="pharmacy_masks")
    mask = relationship("Mask", back_populates="prices")


class User(Base):
    """
    Represents a user.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    cash_balance = Column(Numeric(10, 2), nullable=False)
    transactions = relationship("Transaction", back_populates="user")


class Transaction(Base):
    """
    Represents a transaction.
    """
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False,
                     index=True)
    pharmacy_id = Column(Integer, ForeignKey('pharmacies.id'), nullable=False,
                         index=True)
    mask_id = Column(Integer, ForeignKey('masks.id'), nullable=False,
                     index=True)
    transaction_amount = Column(Numeric(10, 2), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    user = relationship("User", back_populates="transactions")
    pharmacy = relationship("Pharmacy", back_populates="transactions")
    mask = relationship("Mask", back_populates="transactions")
