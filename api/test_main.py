import os
import sys

import pytest
import toml
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, cast, Integer
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ETL import run
from database import Base
from db_models import MaskPrice, Pharmacy, Transaction, User
from main import get_db, app
from tools import install_pg_trgm, TEST_DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_test_data():
    print('setup_and_teardown_test_data')

    db = TestingSessionLocal()
    try:
        install_pg_trgm(engine)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        run(db)
        yield
    finally:
        db.close()


def test_read_pharmacies(client):
    response = client.get("/pharmacies", params={"skip": 1, "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 10
    assert data[0]['id'] != 1


def test_read_masks_by_pharmacy_sorted_by_name(client):
    response = client.get("/pharmacies/1/masks", params={"skip": 0, "limit": 10, "sort_by": "name"})
    assert response.status_code == 200
    data = response.json()
    assert all(item['pharmacy_id'] == 1 for item in data)
    mask_names = [item['mask']['name'] for item in data]
    assert mask_names == sorted(mask_names)


def test_read_pharmacies_by_count_and_range(client):
    min_price = 5
    max_price = 50

    response = client.get("/pharmacies_by_count_and_range",
                          params={
                              "min_count": 2, "max_count": 10,
                              "min_price": min_price, "max_price": max_price
                          })
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    for item in data:
        pharmacy_id = item['id']
        mask_count = item['mask_count']

        actual_mask_count = get_mask_count_in_price_range(pharmacy_id, min_price, max_price)
        assert mask_count == actual_mask_count


def get_mask_count_in_price_range(pharmacy_id, min_price, max_price):
    db = TestingSessionLocal()
    count = db.query(func.count(MaskPrice.id)).filter(
        MaskPrice.pharmacy_id == pharmacy_id,
        MaskPrice.price >= min_price,
        MaskPrice.price <= max_price
    ).scalar()
    db.close()
    return count


def test_read_top_user_amount(client):
    start_date = "2021-01-01"
    end_date = "2021-03-01"

    response = client.get("/top_user_amount", params={"start_date": start_date, "end_date": end_date})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    for item in data:
        user_id = item['id']
        total_amount = item['total_amount']

        actual_total_amount = get_user_total_amount_with_sqlalchemy(user_id, start_date, end_date)

        assert total_amount == actual_total_amount


def get_user_total_amount_with_sqlalchemy(user_id, start_date, end_date):
    db = TestingSessionLocal()
    total_amount = db.query(cast(func.sum(Transaction.transaction_amount), Integer)).filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).scalar()

    db.close()
    return total_amount


def test_read_transactions_summary(client):
    start_date = "2021-01-01"
    end_date = "2021-03-01"

    response = client.get("/transactions/summary", params={"start_date": start_date, "end_date": end_date})
    assert response.status_code == 200
    data = response.json()

    assert 'total_amount' in data
    assert 'total_value' in data

    total_amount = data['total_amount']
    total_value = data['total_value']

    transactions, mask_prices = get_transactions_and_prices_with_sqlalchemy(start_date, end_date)

    actual_total_amount = len(transactions)
    actual_total_value = float(sum(t.transaction_amount for t in transactions))

    assert total_amount == actual_total_amount
    assert total_value == actual_total_value


def get_transactions_and_prices_with_sqlalchemy(start_date, end_date):
    db = TestingSessionLocal()

    transactions = db.query(Transaction).filter(
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()

    mask_prices = {f'{mp.mask_id}{mp.pharmacy_id}': mp.price for mp in db.query(MaskPrice).all()}

    db.close()
    return transactions, mask_prices


def test_search_pharmacies(client):
    search_term = "Care"

    response = client.get("/search", params={"search_term": search_term})
    assert response.status_code == 200
    data = response.json()

    assert len(data) > 0
    for item in data:
        assert search_term.lower() in item['name'].lower()


def test_search_masks(client):
    search_term = "mask"

    response = client.get("/search", params={"search_term": search_term})
    assert response.status_code == 200
    data = response.json()

    assert len(data) > 0
    for item in data:
        assert search_term.lower() in item['name'].lower()


def test_purchase_single_mask(client):
    user_id = 1
    pharmacy_id = 1
    mask_id = 1

    db = TestingSessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
    mask_price_record = db.query(MaskPrice).filter(MaskPrice.mask_id == mask_id,
                                                   MaskPrice.pharmacy_id == pharmacy_id).first()

    assert user is not None, f"User with ID {user_id} not found"
    assert pharmacy is not None, f"Pharmacy with ID {pharmacy_id} not found"
    assert mask_price_record is not None, f"MaskPrice record for mask ID {mask_id} not found"

    initial_user_balance = user.cash_balance
    initial_pharmacy_balance = pharmacy.cash_balance
    mask_price = mask_price_record.price

    db.close()

    response = client.post("/purchase", json={"user_id": user_id, "pharmacy_id": pharmacy_id, "mask_id": mask_id})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    transaction_id = response.json().get('transaction_id')

    expected_user_balance = initial_user_balance - mask_price
    expected_pharmacy_balance = initial_pharmacy_balance + mask_price

    db = TestingSessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    db.close()

    assert user.cash_balance == expected_user_balance
    assert pharmacy.cash_balance == expected_pharmacy_balance
    assert transaction.transaction_amount == mask_price
