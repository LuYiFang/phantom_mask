"""
mask_crud.py
--------

This module contains CRUD operations for managing mask records
in the database.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database import db_models as db_mod
from api.enums import SortType
from api.schemas import input_schema as in_sch, output_schema as out_sch


def get_mask(db: Session, mask_id: int):
    """
    Retrieve a mask by its ID.
    """
    return db.query(db_mod.Mask).filter(db_mod.Mask.id == mask_id).first()


def create_mask(db: Session, mask: db_mod.Mask):
    """
    Create a new mask in the database.
    """
    db.add(mask)
    db.commit()
    db.refresh(mask)
    return mask


def search_masks(db: Session, search_term: str):
    """
    Search for masks by name, using trigrams for fuzzy matching,
    ranked by relevance to the search term.
    """
    return (
        db.query(db_mod.Mask)
        .filter(func.similarity(db_mod.Mask.name, search_term) > 0.1)
        .order_by(func.similarity(db_mod.Mask.name, search_term).desc())
        .all()
    )


def list_pharmacy_masks(
        db: Session,
        pharmacy_id: int,
        sort_by: SortType,
        paging: in_sch.PagingParams,
):
    """
    List all masks sold by a given pharmacy, sorted by mask name or price.
    """
    query = (
        db.query(
            db_mod.PharmacyMask.id,
            db_mod.Mask.name,
            db_mod.PharmacyMask.price
        ).filter(
            db_mod.PharmacyMask.pharmacy_id == pharmacy_id
        ).join(db_mod.Mask)
    )

    if sort_by == SortType.NAME:
        query = query.order_by(db_mod.Mask.name)
    elif sort_by == SortType.PRICE:
        query = query.order_by(db_mod.PharmacyMask.price)

    return query.offset(paging.skip).limit(paging.limit)


def get_mask_summary(
        db: Session,
        date_range: in_sch.DateRange
):
    """
    Retrieve the total amount of masks and dollar value of transactions
    within a date range, grouped by mask.
    """
    result = db.query(
        db_mod.Mask.id.label('mask_id'),
        db_mod.Mask.name.label('mask_name'),
        func.count(db_mod.Transaction.id).label('mask_count'),
        func.sum(db_mod.Transaction.transaction_amount).label('total_value')
    ).filter(
        db_mod.Transaction.date.between(
            date_range.start_date,
            date_range.end_date
        )
    ).join(
        db_mod.Transaction, db_mod.Transaction.mask_id == db_mod.Mask.id
    ).group_by(
        db_mod.Mask.id
    ).all()

    return [out_sch.TransactionSummary(
        mask_id=row.mask_id,
        mask_name=row.mask_name,
        mask_count=row.mask_count,
        total_value=row.total_value) for row in result]
