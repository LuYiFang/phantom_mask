"""
search_route.py
-------------

This module provides API endpoints for interacting with search.
"""

from typing import List

from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.enums import SearchType
from api.schemas import input_schema as in_sch, output_schema as out_sch
from api.services import search_service

router = APIRouter(tags=['Search'])


@router.get("/search", response_model=List[out_sch.SearchResult])
def search_entities(
        search_term: str,
        search_type: SearchType = Query(
            SearchType.ALL,
            description="Type of entity to search: 'pharmacy' or 'mask'"
        ),
        paging: in_sch.PagingParams = Depends(),
        db: Session = Depends(get_db)
):
    """
    Search for pharmacies and masks by name, using trigrams for fuzzy matching,
    ranked by relevance to the search term.
    """
    return search_service.search_entities(db, search_term, search_type, paging)
