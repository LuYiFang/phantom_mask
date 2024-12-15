"""
pharmacy_route.py
-------------

This module provides API endpoints for interacting with pharmacies.
"""

from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.enums import DayOfWeek, SortType
from api.schemas import input_schema as in_sch, output_schema as out_sch
from api.services import pharmacy_service

router = APIRouter(tags=['Pharmacies'])


@router.get("/pharmacies/{pharmacy_id}", response_model=out_sch.Pharmacy)
def read_pharmacy(pharmacy_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a pharmacy by its ID.
    """
    return pharmacy_service.read_pharmacy_details(db, pharmacy_id)


@router.get("/pharmacies", response_model=List[out_sch.Pharmacy])
def list_pharmacies(paging: in_sch.PagingParams,
                    db: Session = Depends(get_db)):
    """
    Retrieve a list of pharmacies with pagination.
    """
    return pharmacy_service.list_pharmacies(db, paging)


@router.get("/pharmacies/open/at", response_model=List[out_sch.Pharmacy])
def list_pharmacies_open_at(
        query_time: in_sch.TimeQuery = Depends(in_sch.get_time),
        day_of_week: DayOfWeek = DayOfWeek.MON,
        paging: in_sch.PagingParams = Depends(),
        db: Session = Depends(get_db)
):
    """
    Retrieve pharmacies open at a specific time and day of the week.
    """
    return pharmacy_service.list_pharmacies_open_at(db, query_time.query_time,
                                                    day_of_week, paging)


@router.get("/pharmacies/{pharmacy_id}/masks",
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
    return pharmacy_service.list_pharmacy_masks(db, pharmacy_id,
                                                sort_by, paging)


@router.post("/pharmacies", response_model=out_sch.Pharmacy)
def create_pharmacy(pharmacy: in_sch.PharmacyCreate,
                    db: Session = Depends(get_db)):
    """
    Create a new pharmacy.
    """
    return pharmacy_service.add_new_pharmacy(db, pharmacy)


@router.get("/pharmacies/search", response_model=List[out_sch.Pharmacy])
def search_pharmacies(search_term: str, db: Session = Depends(get_db)):
    """
    Search for pharmacies by name, ranked by relevance to the search term.
    """
    return pharmacy_service.search_pharmacies(db, search_term)
