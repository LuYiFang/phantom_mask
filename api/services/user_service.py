"""
user_service.py
---------------

This module provides service layer functions for managing user operations.
"""

from sqlalchemy.orm import Session

from api.crud import user_crud
from api.schemas import input_schema as in_sch
from api.utils.tools import exception_handler


@exception_handler
def list_top_users_by_transaction_amount(
        db: Session,
        date_range: in_sch.DateRange,
        limit: int
):
    """
    Retrieve the top x users by total transaction amount of masks within
    a date range.
    """
    return user_crud.list_top_users_by_transaction_amount(db, date_range, limit)
