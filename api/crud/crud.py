"""
crud.py
--------

This module contains CRUD operations for database interactions.
"""

from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import func, cast, Integer, literal, update, Float
from sqlalchemy.orm import Session

import api.schemas.input as schema_in
import api.schemas.output as schema_out
from api.database.db_models import Pharmacy, Mask, Transaction, PharmacyMask, User

from api.utils.tools import exception_handler
from api.utils.utils import get_user_with_lock, get_pharmacy, get_mask_price


@exception_handler
def get_pharmacies(db: Session, paging: schema_in.PagingParams):
    """
    Retrieve a list of pharmacies with pagination.
    """
    return db.query(Pharmacy).offset(paging.skip).limit(paging.limit)


@exception_handler
def get_sold_masks_by_pharmacy(
        db: Session, pharmacy_id: int,
        paging: schema_in.PagingParams,
):
    """
    Retrieve a list of sold masks by a pharmacy with their prices.
    """
    transactions_with_mask_price = (
        db.query(
            Transaction.id,
            Transaction.date,
            Transaction.transaction_amount,
            Transaction.user_id,
            Transaction.pharmacy_id,
            Transaction.mask_id,
            Mask.name.label('mask_name'),
            PharmacyMask.price.label('mask_price')
        )
        .filter(Transaction.pharmacy_id == pharmacy_id)
        .join(Transaction.mask)
        .join(PharmacyMask,
              (Transaction.mask_id == PharmacyMask.mask_id) &
              (Transaction.pharmacy_id == PharmacyMask.pharmacy_id)
              )
        .order_by(Mask.name, PharmacyMask.price)
        .offset(paging.skip)
        .limit(paging.limit)
        .all()
    )

    return [
        {
            "id": t.id,
            "date": t.date,
            "transaction_amount": t.transaction_amount,
            "user_id": t.user_id,
            "pharmacy_id": t.pharmacy_id,
            "mask_id": t.mask_id,
            "mask": {
                "id": t.mask_id,
                "name": t.mask_name,
                "price": t.mask_price
            }
        }
        for t in transactions_with_mask_price
    ]


@exception_handler
def get_pharmacies_by_count_and_range(
        db: Session,
        count: schema_in.CountRangeParams,
        price: schema_in.PriceRangeParams,
        paging: schema_in.PagingParams,
):
    """
    Retrieve pharmacies by mask count and price range with pagination.
    """
    subquery = (
        db.query(
            PharmacyMask.pharmacy_id,
            func.count(PharmacyMask.id).label('mask_count')
        )
        .filter(
            PharmacyMask.price >= price.min_price,
            PharmacyMask.price <= price.max_price
        )
        .group_by(PharmacyMask.pharmacy_id)
        .having(
            func.count(PharmacyMask.id).between(count.min_count, count.max_count)
        )
        .subquery()
    )

    query = (
        db.query(Pharmacy, subquery.c.mask_count)
        .join(subquery, Pharmacy.id == subquery.c.pharmacy_id)
        .offset(paging.skip)
        .limit(paging.limit)
    )

    results = query.all()

    pharmacies_with_mask_count = [
        schema_out.Pharmacy.from_orm(pharmacy).model_dump() | {
            "mask_count": mask_count}
        for pharmacy, mask_count in results
    ]
    return pharmacies_with_mask_count


@exception_handler
def get_top_user_amount(db: Session,
                        date_range: schema_in.DateRange,
                        paging: schema_in.PagingParams
                        ):
    """
    Retrieve the top users by transaction amount within a date range.
    """
    return (db.query(User.id, User.name,
                     cast(func.sum(Transaction.transaction_amount),
                          Integer).label('total_amount')
                     )
            .join(Transaction)
            .filter(Transaction.date >= date_range.start_date,
                    Transaction.date <= date_range.end_date)
            .group_by(User.id)
            .order_by(func.sum(Transaction.transaction_amount).desc())
            .offset(paging.skip).limit(paging.limit))


@exception_handler
def get_transaction_mask_and_value(
        db: Session,
        date_range: schema_in.DateRange
):
    """
    Retrieve the total number of transactions and their total value
    within a date range.
    """
    return db.query(
        func.count(Transaction.transaction_amount).label('total_amount'),
        cast(func.sum(Transaction.transaction_amount), Float).label(
            'total_value')
    ).filter(
        Transaction.date >= date_range.start_date,
        Transaction.date <= date_range.end_date
    ).first()


@exception_handler
def search_pharmacies_and_masks(
        db: Session, search_term: str,
        paging: schema_in.PagingParams
):
    """
    Search for pharmacies and masks by a search term with pagination.
    """
    search_str = f"%{search_term}%"
    results = (
        db.query(
            Pharmacy.id,
            Pharmacy.name,
            literal('pharmacy').label('type')
        )
        .filter(Pharmacy.name.ilike(search_str))
        .union(
            db.query(
                Mask.id,
                Mask.name,
                literal('mask').label('type')
            )
            .filter(Mask.name.ilike(search_str))
        )
        .order_by(func.greatest(
            func.similarity(Pharmacy.name, search_term),
            func.similarity(Mask.name, search_term)
        ).desc())
        .offset(paging.skip).limit(paging.limit)
        .all()
    )

    output = []
    for name_id, name, name_type in results:
        output.append({
            "id": name_id,
            "name": name,
            "type": name_type
        })

    return output


@exception_handler
def purchase_mask(db: Session, purchase_request: schema_in.PurchaseRequest):
    """
    Process a mask purchase transaction.
    """
    user = get_user_with_lock(db, purchase_request.user_id)
    get_pharmacy(db, purchase_request.pharmacy_id)
    mask_price = get_mask_price(db, purchase_request.pharmacy_id,
                                purchase_request.mask_id)

    if user.cash_balance < mask_price.price:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    try:
        db.execute(
            update(User)
            .where(User.id == purchase_request.user_id)
            .values(cash_balance=User.cash_balance - mask_price.price)
        )

        db.execute(
            update(Pharmacy)
            .where(Pharmacy.id == purchase_request.pharmacy_id)
            .values(cash_balance=Pharmacy.cash_balance + mask_price.price)
        )

        transaction = Transaction(
            user_id=purchase_request.user_id,
            pharmacy_id=purchase_request.pharmacy_id,
            mask_id=purchase_request.mask_id,
            transaction_amount=mask_price.price,
            date=datetime.utcnow(),
        )
        db.add(transaction)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,
                            detail="Transaction failed") from e

    return transaction.id
