from typing import List

from pydantic import BaseModel, conint, Field

from schemas.base import PharmacyHourBase, PharmacyBase, MaskBase, MaskPriceBase, TransactionBase, UserBase


class PharmacyHourCreate(PharmacyHourBase):
    pharmacy: str


class PharmacyHour(PharmacyHourBase):
    id: int
    pharmacy_id: int

    class Config:
        orm_mode = True


class Pharmacy(PharmacyBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class PharmacyWithHours(Pharmacy):
    opening_hours: List[PharmacyHour] = []


class PharmacyWithCount(Pharmacy):
    mask_count: int


class Mask(MaskBase):
    id: int

    class Config:
        orm_mode = True


class MaskWithPrice(Mask):
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


class Transaction(TransactionBase):
    id: int
    user_id: int
    pharmacy_id: int
    mask_id: int
    mask: MaskWithPrice

    class Config:
        orm_mode = True


class TransactionSummary(BaseModel):
    total_amount: conint(ge=0) = Field(default=0)
    total_value: float

    class Config:
        orm_mode = True


class TransactionId(BaseModel):
    transaction_id: int

    class Config:
        orm_mode = True


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
