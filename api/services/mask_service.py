"""
mask_service.py
---------------

This module provides service layer functions for managing mask operations.
"""

from sqlalchemy.orm import Session
from api.crud import mask_crud
import api.database.db_models as db_mod
from api.schemas import input_schema as in_sch


def get_mask_details(db: Session, mask_id: int):
    """
    Get detailed information for a specific mask.
    """
    return mask_crud.get_mask(db, mask_id)


def add_new_mask(db: Session, mask_data: in_sch.MaskCreate):
    """
    Add a new mask to the database.
    """
    new_mask = db_mod.Mask(**mask_data.dict())
    return mask_crud.create_mask(db, new_mask)


def search_masks(db: Session, search_term: str):
    """
    Search for masks by name, ranked by relevance to the search term.
    """
    return mask_crud.search_masks(db, search_term)
