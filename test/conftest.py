import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database.database import Base, get_db
import api.database.db_models as db_mod
from api.enums import DayOfWeek
from main import app
from api.utils.tools import install_pg_trgm
from config.config import TEST_DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    install_pg_trgm(engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        pharmacy1 = db_mod.Pharmacy(name="Pharmacy One", cash_balance=150.00)
        pharmacy2 = db_mod.Pharmacy(name="Pharmacy Two", cash_balance=200.00)
        user1 = db_mod.User(name="User One", cash_balance=300.00)
        user2 = db_mod.User(name="User Two", cash_balance=400.00)
        mask1 = db_mod.Mask(name="Adult Mask")
        mask2 = db_mod.Mask(name="Child Mask")
        db.add_all([pharmacy1, pharmacy2, user1, user2, mask1, mask2])
        db.commit()
        db.refresh(pharmacy1)
        db.refresh(pharmacy2)
        db.refresh(user1)
        db.refresh(user2)
        db.refresh(mask1)
        db.refresh(mask2)

        pharmacy_masks = [
            db_mod.PharmacyMask(pharmacy_id=pharmacy1.id, mask_id=mask1.id,
                                price=50),
            db_mod.PharmacyMask(pharmacy_id=pharmacy1.id, mask_id=mask2.id,
                                price=30),
            db_mod.PharmacyMask(pharmacy_id=pharmacy2.id, mask_id=mask1.id,
                                price=70),
            db_mod.PharmacyMask(pharmacy_id=pharmacy2.id, mask_id=mask2.id,
                                price=60)
        ]
        db.add_all(pharmacy_masks)
        db.commit()

        transactions = [
            db_mod.Transaction(user_id=user1.id, pharmacy_id=pharmacy1.id,
                               mask_id=mask1.id, transaction_amount=20.00,
                               date=datetime.datetime(2024, 10, 1)
                               ),
            db_mod.Transaction(user_id=user2.id, pharmacy_id=pharmacy2.id,
                               mask_id=mask2.id, transaction_amount=40.00,
                               date=datetime.datetime(2024, 10, 5)
                               ),
            db_mod.Transaction(user_id=user1.id, pharmacy_id=pharmacy2.id,
                               mask_id=mask1.id, transaction_amount=30.00,
                               date=datetime.datetime(2024, 10, 30)
                               ),
            db_mod.Transaction(user_id=user2.id, pharmacy_id=pharmacy1.id,
                               mask_id=mask2.id, transaction_amount=50.00,
                               date=datetime.datetime(2024, 11, 8)
                               )
        ]
        db.add_all(transactions)
        db.commit()

        pharmacy_hours = [
            db_mod.PharmacyHour(pharmacy_id=pharmacy1.id,
                                day_of_week=DayOfWeek.MON,
                                open_time="08:00:00", close_time="18:00:00"),
            db_mod.PharmacyHour(pharmacy_id=pharmacy1.id,
                                day_of_week=DayOfWeek.TUE,
                                open_time="08:00:00", close_time="18:00:00"),
            db_mod.PharmacyHour(pharmacy_id=pharmacy2.id,
                                day_of_week=DayOfWeek.WED,
                                open_time="09:00:00", close_time="17:00:00"),
            db_mod.PharmacyHour(pharmacy_id=pharmacy2.id,
                                day_of_week=DayOfWeek.THUR,
                                open_time="09:00:00", close_time="17:00:00")
        ]
        db.add_all(pharmacy_hours)
        db.commit()

        yield
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="class")
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="class")
def client():
    with TestClient(app) as c:
        yield c
