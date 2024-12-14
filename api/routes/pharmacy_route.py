"""
pharmacy_route.py
-------------

This module provides API endpoints for interacting with pharmacies.
"""

from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.schemas import input_schema as in_sch, output_schema as out_sch
from api.services import pharmacy_service

router = APIRouter(tags=['Pharmacies'])


@router.get("/pharmacies/{pharmacy_id}", response_model=out_sch.Pharmacy)
def read_pharmacy(pharmacy_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a pharmacy by its ID.
    """
    return pharmacy_service.get_pharmacy_details(db, pharmacy_id)


@router.get("/pharmacies", response_model=List[out_sch.Pharmacy])
def read_pharmacies(paging: in_sch.PagingParams, db: Session = Depends(get_db)):
    """
    Retrieve a list of pharmacies with pagination.
    """
    return pharmacy_service.get_pharmacies(db, paging)


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
