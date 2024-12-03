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
    opening_hours: List[PharmacyHour] = []

    class Config:
        orm_mode = True



class MaskBase(BaseModel):
    name: str


class MaskCreate(MaskBase):
    pass


class Mask(MaskBase):
    id: int

    class Config:
        orm_mode = True


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
    mask: Mask

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    cash_balance: float


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True

