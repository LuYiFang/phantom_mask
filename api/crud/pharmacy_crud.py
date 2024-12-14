"""
pharmacy_crud.py
--------

This module contains CRUD operations for managing pharmacy records
in the database.
"""
from sqlalchemy import func
from sqlalchemy.orm import Session

import api.database.db_models as db_mod
from api.schemas import input_schema as in_sch
from api.utils.tools import exception_handler


def get_pharmacy(db: Session, pharmacy_id: int):
    """
    Retrieve a pharmacy by its ID.
    """
    return db.query(db_mod.Pharmacy).filter(
        db_mod.Pharmacy.id == pharmacy_id).first()


@exception_handler
def get_pharmacies(db: Session, paging: in_sch.PagingParams):
    """
    Retrieve a list of pharmacies with pagination.
    """
    return db.query(db_mod.Pharmacy).offset(paging.skip).limit(paging.limit)


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
