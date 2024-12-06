from fastapi import Query
from pydantic import BaseModel
from typing import List
from datetime import time, datetime


class PharmacyHourBase(BaseModel):
    day_of_week: str
    open_time: time
    close_time: time


class PharmacyHourCreate(PharmacyHourBase):
    pharmacy: str


class PharmacyHour(PharmacyHourBase):
    id: int
    pharmacy_id: int

    class Config:
        orm_mode = True


class PharmacyBase(BaseModel):
    name: str
    cash_balance: float


class PharmacyCreate(PharmacyBase):
    pass


class Pharmacy(PharmacyBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class PharmacyWithHours(Pharmacy):
    opening_hours: List[PharmacyHour] = []


class PharmacyWithCount(Pharmacy):
    mask_count: int


class MaskBase(BaseModel):
    name: str


class MaskCreate(MaskBase):
    pass


class Mask(MaskBase):
    id: int

    class Config:
        orm_mode = True


class MaskWithPrice(Mask):
    price: float


class MaskPriceBase(BaseModel):
    price: float


class MaskPriceCreate(MaskPriceBase):
    pharmacy: str
    mask: str


class MaskPrice(MaskPriceBase):
    id: int
    pharmacy_id: int
    mask_id: int

    class Config:
        orm_mode = True


class PharmacyOrMask(BaseModel):
    id: int
    name: str
    type: str


class TransactionBase(BaseModel):
    transaction_amount: float
    date: datetime


class TransactionCreate(TransactionBase):
    user: str
    pharmacy: str
    mask: str


class Transaction(TransactionBase):
    id: int
    user_id: int
    pharmacy_id: int
    mask_id: int
    mask: MaskWithPrice

    class Config:
        orm_mode = True


class TransactionSummary(BaseModel):
    total_amount: int
    total_value: float

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    cash_balance: float


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserTopCount(BaseModel):
    id: int
    name: str
    total_amount: int

    class Config:
        orm_mode = True


class PurchaseRequest(BaseModel):
    user_id: int
    mask_id: int
    pharmacy_id: int
    amount: int


class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime


def get_date_range(
        start_date: datetime = Query(..., example="2021-01-01"),
        end_date: datetime = Query(..., example="2021-01-31")
) -> DateRange:
    return DateRange(start_date=start_date, end_date=end_date)
