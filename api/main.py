from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import db_models
from database import engine, SessionLocal
from schemas.input import PurchaseRequest, DateRange, get_date_range, PagingParams, CountRangeParams, PriceRangeParams
from schemas.output import PharmacyWithHours, PharmacyWithCount, PharmacyOrMask, Transaction, TransactionSummary, \
    UserTopCount, TransactionId
from tools import install_pg_trgm, generate_openapi_json

db_models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    install_pg_trgm(engine)
    generate_openapi_json(app)
    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pharmacies", response_model=List[PharmacyWithHours])
def read_pharmacies(paging: PagingParams = Depends(), db: Session = Depends(get_db)):
    pharmacies = crud.get_pharmacies(db, **paging.model_dump())
    return pharmacies


@app.get("/pharmacies/{pharmacy_id}/masks", response_model=List[Transaction])
def read_masks_by_pharmacy(pharmacy_id: int, paging: PagingParams = Depends(), db: Session = Depends(get_db)):
    masks = crud.get_sold_masks_by_pharmacy(db, pharmacy_id, **paging.model_dump())
    return masks


@app.get("/pharmacies_by_count_and_range", response_model=List[PharmacyWithCount])
def read_masks_by_count_abd_range(count: CountRangeParams = Depends(),
                                  price: PriceRangeParams = Depends(),
                                  paging: PagingParams = Depends(),
                                  db: Session = Depends(get_db)):
    return crud.get_pharmacies_by_count_and_range(
        db,
        **count.model_dump(),
        **price.model_dump(),
        **paging.model_dump()
    )


@app.get("/top_user_amount", response_model=List[UserTopCount])
def read_top_user_amount(date_range: DateRange = Depends(get_date_range),
                         paging: PagingParams = Depends(),
                         db: Session = Depends(get_db)):
    return crud.get_top_user_amount(db, **date_range.model_dump(), **paging.model_dump())


@app.get("/transactions/summary", response_model=TransactionSummary)
def read_transactions_summary(date_range: DateRange = Depends(get_date_range),
                              db: Session = Depends(get_db)):
    return crud.get_transaction_mask_and_value(db, **date_range.model_dump())


@app.get("/search", response_model=List[PharmacyOrMask])
def search_pharmacies_and_masks(search_term: str,
                                paging: PagingParams = Depends(),
                                db: Session = Depends(get_db)):
    return crud.search_pharmacies_and_masks(db, search_term, **paging.model_dump())


@app.post("/purchase", response_model=TransactionId)
def purchase_masks(purchase_request: PurchaseRequest, db: Session = Depends(get_db)):
    transaction_id = crud.purchase_mask(db, purchase_request)
    return {'transaction_id': transaction_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
