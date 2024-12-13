"""
base.py
-------

This module defines the Pydantic base models for input and output schemas.
These base models are used to validate and serialize the data for
different entities.
"""

from datetime import time, datetime
from pydantic import BaseModel


class PharmacyHourBase(BaseModel):
    """
    Represents the base model for pharmacy operating hours.
    """
    day_of_week: str
    open_time: time
    close_time: time


class PharmacyBase(BaseModel):
    """
    Represents the base model for a pharmacy.
    """
    name: str
    cash_balance: float


class MaskBase(BaseModel):
    """
    Represents the base model for a mask.
    """
    name: str


class MaskPriceBase(BaseModel):
    """
    Represents the base model for a mask price.
    """
    price: float


class TransactionBase(BaseModel):
    """
    Represents the base model for a transaction.
    """
    transaction_amount: float
    date: datetime


class UserBase(BaseModel):
    """
    Represents the base model for a user.
    """
    name: str
    cash_balance: float
