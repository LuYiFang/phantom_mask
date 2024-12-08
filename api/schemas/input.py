from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, PositiveInt, Field, conint

from schemas.base import PharmacyBase, MaskBase, TransactionBase, UserBase


class PurchaseRequest(BaseModel):
    user_id: int
    mask_id: int
    pharmacy_id: int


class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime


def get_date_range(
        start_date: datetime = Query(..., example="2021-01-01"),
        end_date: datetime = Query(..., example="2021-01-31")
) -> DateRange:
    return DateRange(start_date=start_date, end_date=end_date)


class PagingParams(BaseModel):
    skip: conint(ge=0) = Field(default=0)
    limit: PositiveInt = Field(default=10)


class CountRangeParams(BaseModel):
    min_count: conint(ge=0) = Field(default=0)
    max_count: PositiveInt


class PriceRangeParams(BaseModel):
    min_price: float = Field(..., gt=0)
    max_price: float = Field(..., gt=0)


class PharmacyCreate(PharmacyBase):
    pass


class MaskCreate(MaskBase):
    pass


class TransactionCreate(TransactionBase):
    user: str
    pharmacy: str
    mask: str


class UserCreate(UserBase):
    pass
