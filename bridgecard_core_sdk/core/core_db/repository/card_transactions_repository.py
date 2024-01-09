from contextlib import AbstractContextManager
from typing import Callable
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db


TRANSACTIONS_MODEL_NAME = "transactions"


class CardTransactionsRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(
                TRANSACTIONS_MODEL_NAME, db_session.card_transactions_db_app
            )

            self.db_ref = db_ref

    def create_card_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        key_name: str,
        data,
        context,
    ):
        try:

            key = data.get(key_name)

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                card_id
            ).child(key).set(data)

            return True

        except:
            return False


    def fetch_card_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        context,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                card_id
            ).get()
            

            return data

        except:
            return False