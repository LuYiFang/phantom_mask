from typing import List

from pydantic import BaseModel, conint, Field

from schemas.base import PharmacyHourBase, PharmacyBase, MaskBase, MaskPriceBase, TransactionBase, UserBase


class OrmBase(BaseModel):
    class Config:
        from_attributes = True


class PharmacyHourCreate(PharmacyHourBase):
    pharmacy: str


class PharmacyHour(OrmBase, PharmacyHourBase):
    id: int
    pharmacy_id: int


class Pharmacy(OrmBase, PharmacyBase):
    id: int


class PharmacyWithHours(Pharmacy):
    opening_hours: List[PharmacyHour] = []


class PharmacyWithCount(Pharmacy):
    mask_count: int


class Mask(OrmBase, MaskBase):
    id: int


class MaskWithPrice(Mask):
    price: float


class MaskPriceCreate(MaskPriceBase):
    pharmacy: str
    mask: str


class MaskPrice(OrmBase, MaskPriceBase):
    id: int
    pharmacy_id: int
    mask_id: int


class PharmacyOrMask(BaseModel):
    id: int
    name: str
    type: str


class Transaction(OrmBase, TransactionBase):
    id: int
    user_id: int
    pharmacy_id: int
    mask_id: int
    mask: MaskWithPrice


class TransactionSummary(OrmBase, BaseModel):
    total_amount: conint(ge=0) = Field(default=0)
    total_value: float


class TransactionId(OrmBase, BaseModel):
    transaction_id: int


class User(OrmBase, UserBase):
    id: int


class UserTopCount(OrmBase, BaseModel):
    id: int
    name: str
    total_amount: int
