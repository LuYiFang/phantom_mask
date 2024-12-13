"""
input.py
--------

This module defines the Pydantic models for input validation and
data transformation
required for the various API endpoints.
"""

from datetime import datetime
from fastapi import Query
from pydantic import BaseModel, PositiveInt, Field, conint
from schemas.base import PharmacyBase, MaskBase, TransactionBase, UserBase


class PurchaseRequest(BaseModel):
    """
    Represents a purchase request.
    """
    user_id: int
    mask_id: int
    pharmacy_id: int


class DateRange(BaseModel):
    """
    Represents a date range with start and end dates.
    """
    start_date: datetime
    end_date: datetime


def get_date_range(start_date: datetime = Query(..., example="2021-01-01"),
                   end_date: datetime = Query(...,
                                              example="2021-01-31")) -> DateRange:
    """
    Dependency function to get a date range from query parameters.
    """
    return DateRange(start_date=start_date, end_date=end_date)


class PagingParams(BaseModel):
    """
    Represents pagination parameters.
    """
    skip: conint(ge=0) = Field(default=0)
    limit: PositiveInt = Field(default=10)


class CountRangeParams(BaseModel):
    """
    Represents count range parameters.
    """
    min_count: conint(ge=0) = Field(default=0)
    max_count: PositiveInt


class PriceRangeParams(BaseModel):
    """
    Represents price range parameters.
    """
    min_price: float = Field(..., gt=0)
    max_price: float = Field(..., gt=0)


class PharmacyCreate(PharmacyBase):
    """
    Represents the creation of a new pharmacy.
    """


class MaskCreate(MaskBase):
    """
    Represents the creation of a new mask.
    """


class TransactionCreate(TransactionBase):
    """
    Represents the creation of a new transaction.
    """
    user: str
    pharmacy: str
    mask: str


class UserCreate(UserBase):
    """
    Represents the creation of a new user.
    """
