"""
utils.py
--------

This module provides utility functions for interacting with database entities.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.database.db_models import User, Pharmacy, PharmacyMask


def get_user_with_lock(db: Session, user_id: int):
    """
    Retrieve a user by ID with a database lock.
    """
    user = db.query(User).filter(User.id == user_id).with_for_update().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_pharmacy(db: Session, pharmacy_id: int):
    """
    Retrieve a pharmacy by ID.
    """
    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")
    return pharmacy


def get_mask_price(db: Session, pharmacy_id: int, mask_id: int):
    """
    Retrieve the price of a mask at a specific pharmacy.
    """
    mask_price = db.query(PharmacyMask).filter(
        PharmacyMask.pharmacy_id == pharmacy_id,
        PharmacyMask.mask_id == mask_id
    ).first()
    if not mask_price:
        raise HTTPException(status_code=404, detail="Mask price not found")
    return mask_price
