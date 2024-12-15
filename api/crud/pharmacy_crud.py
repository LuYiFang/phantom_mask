"""
pharmacy_crud.py
--------

This module contains CRUD operations for managing pharmacy records
in the database.
"""
from datetime import time

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

import api.database.db_models as db_mod
from api.enums import DayOfWeek, ComparisonType
from api.schemas import input_schema as in_sch


def get_pharmacy(db: Session, pharmacy_id: int):
    """
    Retrieve a pharmacy by its ID.
    """
    return (
        db.query(db_mod.Pharmacy)
        .filter(db_mod.Pharmacy.id == pharmacy_id)
        .first()
    )


def list_pharmacies(db: Session, paging: in_sch.PagingParams):
    """
    Retrieve a list of pharmacies with pagination.
    """
    return db.query(db_mod.Pharmacy).offset(paging.skip).limit(paging.limit)


def list_pharmacies_open_at(
        db: Session,
        query_time: time,
        day_of_week: DayOfWeek,
        paging: in_sch.PagingParams,
):
    """
    Retrieve pharmacies open at a specific time and day of the week.
    """
    return db.query(db_mod.Pharmacy).join(db_mod.PharmacyHour).filter(
        and_(
            db_mod.PharmacyHour.day_of_week == day_of_week,
            db_mod.PharmacyHour.open_time <= query_time,
            db_mod.PharmacyHour.close_time >= query_time
        )
    ).offset(paging.skip).limit(paging.limit)


def list_pharmacies_by_mask_count(
        db: Session,
        comparison: ComparisonType,
        count: int,
        price_range: in_sch.PriceRangeParams,
        paging: in_sch.PagingParams
):
    """
    Retrieve pharmacies with more or less than x mask products within a price range.
    """
    subquery = db.query(
        db_mod.PharmacyMask.pharmacy_id,
        func.count(db_mod.PharmacyMask.id).label("mask_count")
    ).filter(
        # Includes both min_price and max_price
        db_mod.PharmacyMask.price.between(
            price_range.min_price,
            price_range.max_price
        )
    ).group_by(
        db_mod.PharmacyMask.pharmacy_id
    ).subquery()

    query = db.query(
        db_mod.Pharmacy.id,
        db_mod.Pharmacy.name,
        subquery.c.mask_count
    ).join(
        subquery,
        db_mod.Pharmacy.id == subquery.c.pharmacy_id
    )

    if comparison == ComparisonType.MORE:
        query = query.filter(subquery.c.mask_count > count)
    elif comparison == ComparisonType.LESS:
        query = query.filter(subquery.c.mask_count < count)

    return query.offset(paging.skip).limit(paging.limit)


def create_pharmacy(db: Session, pharmacy: db_mod.Pharmacy):
    """
    Create a new pharmacy in the database.
    """
    db.add(pharmacy)
    db.commit()
    db.refresh(pharmacy)
    return pharmacy


def search_pharmacies(db: Session, search_term: str):
    """
    Search for pharmacies by name, using trigrams for fuzzy matching,
    ranked by relevance to the search term.
    """
    return (
        db.query(db_mod.Pharmacy)
        .filter(func.similarity(db_mod.Pharmacy.name, search_term) > 0.1)
        .order_by(
            func.similarity(db_mod.Pharmacy.name, search_term).desc()
        )
        .all()
    )
