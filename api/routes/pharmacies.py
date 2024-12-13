"""
pharmacies.py
-------------

This module provides API endpoints for interacting with pharmacies.
"""

from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from crud import crud as _crud
from database.database import get_db
from schemas.input import (PagingParams, CountRangeParams, PriceRangeParams,
                           PurchaseRequest)
from schemas.output import (PharmacyWithHours, Transaction, PharmacyWithCount,
                            PharmacyOrMask, TransactionId)

router = APIRouter()


@router.get("/pharmacies", response_model=List[PharmacyWithHours])
def read_pharmacies(paging: PagingParams = Depends(),
                    db: Session = Depends(get_db)) -> List[PharmacyWithHours]:
    """
    Retrieve a list of pharmacies with pagination.
    """
    pharmacies = _crud.get_pharmacies(db, **paging.model_dump())
    return pharmacies


@router.get("/pharmacies/{pharmacy_id}/masks",
            response_model=List[Transaction])
def read_masks_by_pharmacy(pharmacy_id: int, paging: PagingParams = Depends(),
                           db: Session = Depends(get_db)) -> List[Transaction]:
    """
    Retrieve a list of masks sold by a specific pharmacy with pagination.
    """
    masks = _crud.get_sold_masks_by_pharmacy(db, pharmacy_id,
                                            **paging.model_dump())
    return masks


@router.get("/pharmacies_by_count_and_range",
            response_model=List[PharmacyWithCount])
def read_masks_by_count_abd_range(count: CountRangeParams = Depends(),
                                  price: PriceRangeParams = Depends(),
                                  paging: PagingParams = Depends(),
                                  db: Session = Depends(get_db)) -> \
        List[PharmacyWithCount]:
    """
    Retrieve pharmacies by mask count and price range with pagination.
    """
    return _crud.get_pharmacies_by_count_and_range(
        db,
        **count.model_dump(),
        **price.model_dump(),
        **paging.model_dump()
    )


@router.get("/search", response_model=List[PharmacyOrMask])
def search_pharmacies_and_masks(search_term: str,
                                paging: PagingParams = Depends(),
                                db: Session = Depends(get_db)) -> (
        List)[PharmacyOrMask]:
    """
    Search for pharmacies and masks by a search term with pagination.
    """
    return _crud.search_pharmacies_and_masks(db, search_term,
                                            **paging.model_dump())


@router.post("/purchase", response_model=TransactionId)
def purchase_masks(purchase_request: PurchaseRequest,
                   db: Session = Depends(get_db)) -> TransactionId:
    """
    Process a mask purchase transaction.
    """
    transaction_id = _crud.purchase_mask(db, purchase_request)
    return {'transaction_id': transaction_id}
