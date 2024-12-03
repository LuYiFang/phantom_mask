from sqlalchemy.orm import Session

from db_models import Pharmacy


def get_pharmacies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pharmacy).offset(skip).limit(limit)
