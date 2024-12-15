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
from api.utils.tools import exception_handler


@exception_handler
def read_pharmacy_details(db: Session, pharmacy_id: int):
    """
    Get detailed information for a specific pharmacy.
    """
    return pharmacy_crud.read_pharmacy(db, pharmacy_id)


@exception_handler
def list_pharmacies(
        db: Session,
        paging: in_sch.PagingParams
):
    """
    Get a list of pharmacies with pagination.
    """
    return pharmacy_crud.list_pharmacies(db, paging)


@exception_handler
def list_pharmacies_open_at(
        db: Session,
        query_time: time,
        day_of_week: DayOfWeek,
        paging: in_sch.PagingParams,
):
    """
    Retrieve pharmacies open at a specific time and day of the week.
    """
    return pharmacy_crud.list_pharmacies_open_at(db, query_time, day_of_week,
                                                 paging)


@exception_handler
def list_pharmacy_masks(
        db: Session,
        pharmacy_id: int,
        sort_by: str,
        paging: in_sch.PagingParams,
):
    """
    List all masks sold by a given pharmacy, sorted by mask name or price.
    """
    return pharmacy_crud.list_pharmacy_masks(db, pharmacy_id, sort_by, paging)


@exception_handler
def add_new_pharmacy(
        db: Session,
        pharmacy_data: in_sch.PharmacyCreate
):
    """
    Add a new pharmacy to the database.
    """
    new_pharmacy = db_mod.Pharmacy(**pharmacy_data.dict())
    return pharmacy_crud.create_pharmacy(db, new_pharmacy)


@exception_handler
def search_pharmacies(db: Session, search_term: str):
    """
    Search for pharmacies by name, ranked by relevance to the search term.
    """
    return pharmacy_crud.search_pharmacies(db, search_term)
