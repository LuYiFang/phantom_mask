"""
mask_service.py
---------------

This module provides service layer functions for managing mask operations.
"""

from sqlalchemy.orm import Session

import api.crud.mask_crud
import api.database.db_models as db_mod
from api.crud import mask_crud
from api.enums import SortType
from api.schemas import input_schema as in_sch
from api.utils.tools import exception_handler


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


@exception_handler
def list_pharmacy_masks(
        db: Session,
        pharmacy_id: int,
        sort_by: SortType,
        paging: in_sch.PagingParams,
):
    """
    List all masks sold by a given pharmacy, sorted by mask name or price.
    """
    return api.crud.mask_crud.list_pharmacy_masks(db, pharmacy_id, sort_by, paging)


@exception_handler
def get_mask_summary(
        db: Session,
        date_range: in_sch.DateRange
):
    """
    Get the total amount of masks and dollar value of transactions within
    a date range.
    """
    return api.crud.mask_crud.get_mask_summary(db, date_range)
