from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db


NAIRA_ACCOUNTS_MODEL_NAME = "naira_accounts"


class NairaAccountsRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(
                NAIRA_ACCOUNTS_MODEL_NAME, db_session.naira_accounts_db_app
            )

            self.db_ref = db_ref

    def create_naira_accounts_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_number: str,
        key_name: str,
        data,
        context: Optional[Any] = None,
    ):
        try:

            key = data.get(key_name)

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                account_number
            ).child(key).set(data)

            return True

        except:
            return False
