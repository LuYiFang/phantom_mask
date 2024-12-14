"""
mask_crud.py
--------

This module contains CRUD operations for managing mask records
in the database.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

import api.database.db_models as db_mod


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
