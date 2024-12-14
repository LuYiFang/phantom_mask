import os
from typing import List

import json
from dateutil.parser import parse
import re

from sqlalchemy.orm import Session

from api.database.database import SessionLocal
from api.database.db_models import Pharmacy, Mask, PharmacyMask, PharmacyHour, Transaction, User
from api.schemas.input import PharmacyCreate, TransactionCreate, UserCreate
from api.schemas.output import PharmacyHourCreate, MaskPriceCreate


def load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def parse_pharmacies(data):
    full_days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    def expand_days(days_part):
        if '-' in days_part:
            start_day, end_day = list(map(lambda x: x.strip(), days_part.split('-')))
            start_idx = full_days.index(start_day)
            end_idx = full_days.index(end_day)
            return full_days[start_idx:end_idx + 1]

        return list(map(lambda x: x.strip(), days_part.split(',')))

    pharmacies = []
    masks = {}
    prices = []
    pharmacy_hours = []
    for pharmacy in data:
        pharmacies.append(PharmacyCreate(
            name=pharmacy.get('name'),
            cash_balance=pharmacy.get('cashBalance')
        ))
        for mask in pharmacy.get('masks'):
            masks[mask.get('name')] = 1
            prices.append(MaskPriceCreate(
                pharmacy=pharmacy.get('name'),
                mask=mask.get('name'),
                price=mask.get('price')
            ))

        segments = pharmacy.get('openingHours').split('/')
        for segment in segments:
            match = re.match(r'(.+?) (\d{2}:\d{2}) - (\d{2}:\d{2})', segment)
            days_part, open_time, close_time = match.groups()
            days = expand_days(days_part)
            for day in days:
                pharmacy_hours.append(PharmacyHourCreate(
                    pharmacy=pharmacy.get('name'),
                    day_of_week=day,
                    open_time=open_time,
                    close_time=close_time))
    return pharmacies, pharmacy_hours, list(masks.keys()), prices


def parse_users(data):
    users = []
    transactions = []
    for user in data:
        users.append(UserCreate(
            name=user.get('name'),
            cash_balance=user.get('cashBalance')
        ))
        for transaction in user.get('purchaseHistories'):
            transactions.append(TransactionCreate(
                user=user.get('name'),
                pharmacy=transaction.get('pharmacyName'),
                mask=transaction.get('maskName'),
                transaction_amount=transaction.get('transactionAmount'),
                date=parse(transaction.get('transactionDate')),
            ))
    return users, transactions


def insert_data(
        db: Session,
        pharmacies: List[PharmacyCreate],
        pharmacy_hours: List[PharmacyHourCreate],
        masks: list[str],
        prices: List[MaskPriceCreate],
        users: List[UserCreate],
        transactions: List[TransactionCreate]
):
    try:

        for pharmacy in pharmacies:
            db.add(Pharmacy(**pharmacy.model_dump()))

        for mask in masks:
            db.add(Mask(
                name=mask,
            ))

        for user in users:
            db.add(User(**user.model_dump()))

        db.commit()

        pharmacy_dict = {pharmacy.name: pharmacy.id for pharmacy in db.query(Pharmacy).all()}
        mask_dict = {mask.name: mask.id for mask in db.query(Mask).all()}
        user_dict = {user.name: user.id for user in db.query(User).all()}

        for price in prices:
            db.add(PharmacyMask(
                pharmacy_id=pharmacy_dict[price.pharmacy],
                mask_id=mask_dict[price.mask],
                price=price.price,
            ))

        for hours in pharmacy_hours:
            db.add(PharmacyHour(
                pharmacy_id=pharmacy_dict[hours.pharmacy],
                day_of_week=hours.day_of_week,
                open_time=hours.open_time,
                close_time=hours.close_time,
            ))

        for transaction in transactions:
            db.add(Transaction(
                user_id=user_dict[transaction.user],
                pharmacy_id=pharmacy_dict[transaction.pharmacy],
                mask_id=mask_dict[transaction.mask],
                transaction_amount=transaction.transaction_amount,
                date=transaction.date,
            ))

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def run(db):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pharmacies_path = os.path.join(current_dir, 'data/pharmacies.json')
    pharmacy_raw = load_data(pharmacies_path)
    pharmacies, pharmacy_hours, masks, prices = parse_pharmacies(pharmacy_raw)

    users_path = os.path.join(current_dir, 'data/users.json')
    user_raw = load_data(users_path)
    users, transactions = parse_users(user_raw)

    insert_data(db, pharmacies, pharmacy_hours, masks, prices, users, transactions)


if __name__ == "__main__":
    db: Session = SessionLocal()
    run(db)
