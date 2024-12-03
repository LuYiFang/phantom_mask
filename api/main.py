from fastapi import FastAPI, Depends
from typing import List

from sqlalchemy.orm import Session

import crud
import db_models
from database import engine, SessionLocal
from in_out_schema import Pharmacy, Transaction

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pharmacies", response_model=List[Pharmacy])
def read_pharmacies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pharmacies = crud.get_pharmacies(db, skip=skip, limit=limit)
    return pharmacies


@app.get("/pharmacies/{pharmacy_id}/masks", response_model=List[Transaction])
def read_masks_by_pharmacy(pharmacy_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    masks = crud.get_sold_masks_by_pharmacy(db, pharmacy_id=pharmacy_id, skip=skip, limit=limit)
    return masks


@app.get("/pharmacies_by_mask_count_and_price_range/", response_model=List[Pharmacy])
def read_pharmacies_by_mask_count_and_price_range(min_count: int, max_count: int,
                                                  min_price: float, max_price: float,
                                                  db: Session = Depends(get_db)):
    pharmacies = crud.get_masks_by_count_abd_range(db, min_count=min_count, max_count=max_count, min_price=min_price,
                                                   max_price=max_price)
    return pharmacies


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)

