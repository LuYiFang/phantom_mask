"""
pharmacy_service.py
--------------------

This module provides service layer functions for managing pharmacy operations.
"""
from datetime import time

from sqlalchemy.orm import Session
from api.crud import pharmacy_crud
import api.database.db_models as db_mod
from api.enums import DayOfWeek
from api.schemas import input_schema as in_sch


def get_pharmacy_details(db: Session, pharmacy_id: int):
    """
    Get detailed information for a specific pharmacy.
    """
    return pharmacy_crud.get_pharmacy(db, pharmacy_id)


def get_pharmacies(
        db: Session,
        paging: in_sch.PagingParams
):
    """
    Get a list of pharmacies with pagination.
    """
    return pharmacy_crud.get_pharmacies(db, paging)


def get_pharmacies_open_at(
        db: Session,
        query_time: time,
        day_of_week: DayOfWeek,
        paging: in_sch.PagingParams,
):
    """
    Retrieve pharmacies open at a specific time and day of the week.
    """
    return pharmacy_crud.get_pharmacies_open_at(db, query_time, day_of_week, paging)


def add_new_pharmacy(
        db: Session,
        pharmacy_data: in_sch.PharmacyCreate
):
    """
    Add a new pharmacy to the database.
    """
    new_pharmacy = db_mod.Pharmacy(**pharmacy_data.dict())
    return pharmacy_crud.create_pharmacy(db, new_pharmacy)


def search_pharmacies(db: Session, search_term: str):
    """
    Search for pharmacies by name, ranked by relevance to the search term.
    """
    return pharmacy_crud.search_pharmacies(db, search_term)
