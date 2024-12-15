"""
user_crud.py
--------

This module contains CRUD operations for managing user records
in the database.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database import db_models as db_mod
from api.schemas import input_schema as in_sch, output_schema as out_sch


def list_top_users_by_transaction_amount(
        db: Session,
        date_range: in_sch.DateRange,
        limit: int
):
    """
    Retrieve the top x users by total transaction amount of masks within
    a date range.
    """
    result = db.query(
        db_mod.User.id,
        db_mod.User.name,
        func.sum(db_mod.Transaction.transaction_amount).label('total_amount')
    ).join(
        db_mod.Transaction
    ).filter(
        db_mod.Transaction.date.between(
            date_range.start_date,
            date_range.end_date
        )
    ).group_by(
        db_mod.User.id
    ).order_by(
        func.sum(db_mod.Transaction.transaction_amount).desc()
    ).limit(limit)

    return [out_sch.UserTransactionSummary(
        id=row.id,
        name=row.name,
        total_amount=row.total_amount)
        for row in result]
