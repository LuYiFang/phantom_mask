"""
transaction_route.py
---------------

This module provides API endpoints for interacting with transactions
and user amounts.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.database.database import get_db
from api.services import transaction_service
from api.schemas import output_schema as out_sch

router = APIRouter(tags=["Transactions"])


@router.get("/transactions/{transaction_id}",
            response_model=out_sch.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a transaction by its ID.
    """
    return transaction_service.get_transaction_details(db, transaction_id)
