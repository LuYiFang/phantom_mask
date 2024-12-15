"""
search_service.py
------------------------

This module provides service layer functions for managing search operations.
"""
from sqlalchemy import desc
from sqlalchemy.orm import Session

from api.crud import mask_crud, pharmacy_crud
from api.enums import SearchType
from api.schemas import input_schema as in_sch


def search_entities(
        db: Session,
        search_term: str,
        search_type: SearchType,
        paging: in_sch.PagingParams
):
    queries = []
    if search_type in {SearchType.PHARMACY, SearchType.ALL}:
        pharmacies = pharmacy_crud.search_pharmacies(db, search_term)
        queries.append(pharmacies)

    if search_type in {SearchType.MASK, SearchType.ALL}:
        masks = mask_crud.search_masks(db, search_term)
        queries.append(masks)

    results = []
    if queries:
        results = queries[0].union_all(*queries[1:]).order_by(
            desc('similarity')).offset(paging.skip).limit(paging.limit)

    return results
