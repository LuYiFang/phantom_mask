"""
transaction_crud.py
--------------------

This module contains CRUD operations for managing transaction records
in the database.
"""
from sqlalchemy.orm import Session

import api.database.db_models as db_mod


def get_transaction(db: Session, transaction_id: int):
    """
    Retrieve a transaction by its ID.
    """
    return (
        db.query(db_mod.Transaction)
        .filter(db_mod.Transaction.id == transaction_id).first()
    )


def create_transaction(db: Session, transaction: db_mod.Transaction):
    """
    Create a new transaction in the database.
    """
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
