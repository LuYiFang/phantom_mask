from typing import List, Dict

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import db_models
from database import engine, SessionLocal
from in_out_schema import PharmacyWithHours, Transaction, PharmacyWithCount, UserTopCount, DateRange, \
    get_date_range, TransactionSummary, PharmacyOrMask, PurchaseRequest

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pharmacies", response_model=List[PharmacyWithHours])
def read_pharmacies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pharmacies = crud.get_pharmacies(db, skip=skip, limit=limit)
    return pharmacies


@app.get("/pharmacies/{pharmacy_id}/masks", response_model=List[Transaction])
def read_masks_by_pharmacy(pharmacy_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    masks = crud.get_sold_masks_by_pharmacy(db, pharmacy_id=pharmacy_id, skip=skip, limit=limit)
    return masks


@app.get("/pharmacies_by_count_and_range", response_model=List[PharmacyWithCount])
def read_masks_by_count_abd_range(min_count: int, max_count: int,
                                  min_price: float, max_price: float,
                                  skip: int = 0, limit: int = 10,
                                  db: Session = Depends(get_db)):
    return crud.get_pharmacies_by_count_and_range(db,
                                                  min_count, max_count,
                                                  min_price, max_price,
                                                  skip, limit)


@app.get("/top_user_amount", response_model=List[UserTopCount])
def read_top_user_amount(
        date_range: DateRange = Depends(get_date_range),
        limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_user_amount(db, date_range.start_date, date_range.end_date, limit)


@app.get("/transactions/summary", response_model=TransactionSummary)
def read_transactions_summary(
        date_range: DateRange = Depends(get_date_range),
        db: Session = Depends(get_db)):
    return crud.get_transaction_mask_and_value(db, date_range.start_date, date_range.end_date)


@app.get("/search", response_model=List[PharmacyOrMask])
def search_pharmacies_and_masks(search_term: str, limit: int = 10, db: Session = Depends(get_db)):
    return crud.search_pharmacies_and_masks(db, search_term, limit)


@app.post("/purchase", response_model=Dict[str, int])
def purchase_masks(purchase_request: PurchaseRequest, db: Session = Depends(get_db)):
    transaction_id = crud.purchase_mask(db, purchase_request)
    return {'transaction_id': transaction_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
