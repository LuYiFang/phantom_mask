"""
transactions.py
---------------

This module provides API endpoints for interacting with transactions
and user amounts.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import crud
from database.database import get_db
from schemas.input import DateRange, get_date_range, PagingParams
from schemas.output import UserTopCount, TransactionSummary

router = APIRouter()


@router.get("/top_user_amount", response_model=List[UserTopCount])
def read_top_user_amount(date_range: DateRange = Depends(get_date_range),
                         paging: PagingParams = Depends(),
                         db: Session = Depends(get_db)) -> List[UserTopCount]:
    """
    Retrieve the top users by transaction amount within a date range.
    """
    return crud.get_top_user_amount(db, **date_range.model_dump(),
                                    **paging.model_dump())


@router.get("/transactions/summary", response_model=TransactionSummary)
def read_transactions_summary(date_range: DateRange = Depends(get_date_range),
                              db: Session = Depends(
                                  get_db)) -> TransactionSummary:
    """
    Retrieve the total number of transactions and their total value within a date range.
    """
    return crud.get_transaction_mask_and_value(db, **date_range.model_dump())
