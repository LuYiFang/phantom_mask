"""
transactions_service.py
------------------------

This module provides service layer functions for managing transaction operations.
"""

from sqlalchemy.orm import Session
from api.crud import transaction_crud
import api.database.db_models as db_mod
from api.schemas import input_schema as in_sch
from api.utils.tools import exception_handler


@exception_handler
def get_transaction_details(db: Session, transaction_id: int):
    """
    Get detailed information for a specific transaction.
    """
    return transaction_crud.get_transaction(db, transaction_id)


@exception_handler
def create_transaction(
        db: Session,
        transaction_data: in_sch.TransactionCreate
):
    """
    Create a new transaction to the database.
    """
    new_transaction = db_mod.Transaction(**transaction_data.dict())
    return transaction_crud.create_transaction(db, new_transaction)
