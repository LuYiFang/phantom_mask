from typing import List, Dict

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import db_models
from database import engine, SessionLocal
from schemas.input import PurchaseRequest, DateRange, get_date_range, PagingParams, CountRangeParams, PriceRangeParams
from schemas.output import PharmacyWithHours, PharmacyWithCount, PharmacyOrMask, Transaction, TransactionSummary, \
    UserTopCount

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pharmacies", response_model=List[PharmacyWithHours])
def read_pharmacies(paging: PagingParams = Depends(), db: Session = Depends(get_db)):
    pharmacies = crud.get_pharmacies(db, **paging.dict())
    return pharmacies


@app.get("/pharmacies/{pharmacy_id}/masks", response_model=List[Transaction])
def read_masks_by_pharmacy(pharmacy_id: int, paging: PagingParams = Depends(), db: Session = Depends(get_db)):
    masks = crud.get_sold_masks_by_pharmacy(db, pharmacy_id, **paging.dict())
    return masks


@app.get("/pharmacies_by_count_and_range", response_model=List[PharmacyWithCount])
def read_masks_by_count_abd_range(count: CountRangeParams = Depends(),
                                  price: PriceRangeParams = Depends(),
                                  paging: PagingParams = Depends(),
                                  db: Session = Depends(get_db)):
    return crud.get_pharmacies_by_count_and_range(
        db,
        **count.dict(),
        **price.dict(),
        **paging.dict()
    )


@app.get("/top_user_amount", response_model=List[UserTopCount])
def read_top_user_amount(date_range: DateRange = Depends(get_date_range),
                         paging: PagingParams = Depends(),
                         db: Session = Depends(get_db)):
    return crud.get_top_user_amount(db, **date_range.dict(), **paging.dict())


@app.get("/transactions/summary", response_model=TransactionSummary)
def read_transactions_summary(date_range: DateRange = Depends(get_date_range),
                              db: Session = Depends(get_db)):
    return crud.get_transaction_mask_and_value(db, **date_range.dict())


@app.get("/search", response_model=List[PharmacyOrMask])
def search_pharmacies_and_masks(search_term: str,
                                paging: PagingParams = Depends(),
                                db: Session = Depends(get_db)):
    return crud.search_pharmacies_and_masks(db, search_term, **paging.dict())


@app.post("/purchase", response_model=Dict[str, int])
def purchase_masks(purchase_request: PurchaseRequest, db: Session = Depends(get_db)):
    transaction_id = crud.purchase_mask(db, purchase_request)
    return {'transaction_id': transaction_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
