from sqlalchemy.orm import Session
from fastapi import HTTPException
from db_models import User, Pharmacy, MaskPrice


def get_user_with_lock(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).with_for_update().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_pharmacy(db: Session, pharmacy_id: int):
    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")
    return pharmacy


def get_mask_price(db: Session, pharmacy_id: int, mask_id: int):
    mask_price = db.query(MaskPrice).filter(
        MaskPrice.pharmacy_id == pharmacy_id,
        MaskPrice.mask_id == mask_id
    ).first()
    if not mask_price:
        raise HTTPException(status_code=404, detail="Mask price not found")
    return mask_price
