from datetime import time, datetime

from pydantic import BaseModel


class PharmacyHourBase(BaseModel):
    day_of_week: str
    open_time: time
    close_time: time


class PharmacyBase(BaseModel):
    name: str
    cash_balance: float


class MaskBase(BaseModel):
    name: str


class MaskPriceBase(BaseModel):
    price: float


class TransactionBase(BaseModel):
    transaction_amount: float
    date: datetime


class UserBase(BaseModel):
    name: str
    cash_balance: float


