"""
mask_routes.py
--------------

This module defines the API endpoints for managing masks.
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.enums import SortType
from api.schemas import input_schema as in_sch, output_schema as out_sch
from api.services import mask_service

router = APIRouter(tags=['Masks'])


@router.get("/masks/{mask_id}", response_model=out_sch.Mask)
def read_mask(mask_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a mask by its ID.
    """
    return mask_service.get_mask_details(db, mask_id)


@router.post("/masks", response_model=out_sch.Mask)
def create_mask(mask: in_sch.MaskCreate, db: Session = Depends(get_db)):
    """
    Create a new mask.
    """
    return mask_service.create_mask(db, mask)


@router.get("/masks/pharmacies/{pharmacy_id}",
            response_model=List[out_sch.MaskWithPrice])
def list_pharmacy_masks(
        pharmacy_id: int,
        sort_by: SortType = SortType.NAME,
        paging: in_sch.PagingParams = Depends(),
        db: Session = Depends(get_db)
):
    """
    List all masks sold by a given pharmacy, sorted by mask name or price.
    """
    return mask_service.list_pharmacy_masks(db, pharmacy_id,
                                                         sort_by, paging)


@router.get("/masks/transactions/summary",
            response_model=List[out_sch.TransactionSummary])
def get_mask_summary(
        date_range: in_sch.DateRange = Depends(in_sch.get_date_range),
        db: Session = Depends(get_db)
):
    """
    Retrieve the total amount of masks and dollar value of transactions within
    a date range.
    """
    return mask_service.get_mask_summary(db, date_range)
