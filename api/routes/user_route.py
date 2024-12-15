"""
user_routes.py
--------------

This module defines the API endpoints for managing users.
"""
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.schemas import input_schema as in_sch, output_schema as out_sch
from api.services import user_service

router = APIRouter(tags=['Users'])


@router.get("/users/transaction_amount",
            response_model=List[out_sch.UserTransactionSummary])
def list_top_users_by_transaction_amount(
        date_range: in_sch.DateRange = Depends(in_sch.get_date_range),
        limit: int = Query(10,
                           description="The number of top users to return"),
        db: Session = Depends(get_db)
):
    """
    Retrieve the top x users by total transaction amount of masks within
    a date range.
    """
    return user_service.list_top_users_by_transaction_amount(db, date_range,
                                                             limit)
