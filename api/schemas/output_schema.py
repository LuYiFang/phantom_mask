"""
output_schema.py
---------

This module defines the Pydantic models for output schemas.
"""

from typing import List
from pydantic import BaseModel, conint, Field
from api.schemas.base_schema import (PharmacyHourBase, PharmacyBase, MaskBase,
                                     PharmacyMaskBase, TransactionBase,
                                     UserBase)


class OrmBase(BaseModel):
    """
    Base class for ORM models.
    """

    class Config:
        """
        Pydantic configuration class for ORM models.
        """
        from_attributes = True


class PharmacyHour(OrmBase, PharmacyHourBase):
    """
    Model representing pharmacy hours.
    """
    id: int
    pharmacy_id: int


class Pharmacy(OrmBase, PharmacyBase):
    """
    Model representing a pharmacy.
    """
    id: int


class PharmacyDetail(Pharmacy):
    """
    Model representing a pharmacy detail.
    """
    cash_balance: float
    opening_hours: List[PharmacyHour] = []


class PharmacyWithHours(Pharmacy):
    """
    Model representing a pharmacy with its hours.
    """
    opening_hours: List[PharmacyHour] = []


class PharmacyWithCount(Pharmacy):
    """
    Model representing a pharmacy with mask count.
    """
    mask_count: int


class Mask(OrmBase, MaskBase):
    """
    Model representing a mask.
    """
    id: int


class MaskWithPrice(Mask):
    """
    Model representing a mask with its price.
    """
    price: float


class PharmacyMask(OrmBase, PharmacyMaskBase):
    """
    Model representing a mask price.
    """
    id: int
    pharmacy_id: int
    mask_id: int


class PharmacyOrMask(BaseModel):
    """
    Model representing either a pharmacy or a mask in search results.
    """
    id: int
    name: str
    type: str


class Transaction(OrmBase, TransactionBase):
    """
    Model representing a transaction.
    """
    id: int
    user_id: int
    pharmacy_id: int
    mask_id: int
    mask: MaskWithPrice


class TransactionSummary(OrmBase, BaseModel):
    """
    Model summarizing transactions.
    """
    mask_id: int
    mask_name: str
    mask_count: int
    total_value: float


class TransactionId(OrmBase, BaseModel):
    """
    Model representing a transaction ID.
    """
    transaction_id: int


class User(OrmBase, UserBase):
    """
    Model representing a user.
    """
    id: int


class UserTransactionSummary(OrmBase, BaseModel):
    """
    Model representing the top users by transaction amount.
    """
    id: int
    name: str
    total_amount: float
