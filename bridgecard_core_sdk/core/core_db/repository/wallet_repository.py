from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

WALLET_MODEL_NAME = "wallets"


class WalletRepository(BaseRepository):

    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(WALLET_MODEL_NAME, db_session.wallets_db_app)

            self.db_ref = db_ref

    def fetch_wallet_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).child(wallet_id).get()

            return data

        except:

            return None

    def set_wallet_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).child(wallet_id).set(value)

            return data

        except:

            return None

    def fetch_wallet_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).child(wallet_id).child(attribute).get()

            return data

        except:
            return None

    def set_wallet_child_atrr_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).child(wallet_id).child(child_atrr).set(value)

            return data

        except:

            return None

    def set_wallet_child_atrr_data_as_transaction(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                wallet_id).child(child_atrr).transaction(lambda current_value: current_value - float(value))

            return data

        except:

            return None

    def wallet_order_by_child(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        child_atrr: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).order_by_child(child_atrr).equal_to(value).get()

            return data

        except:

            return None

    def delete_wallet(self,
                      environment: EnvironmentEnum,
                      company_issuing_app_id: str,
                      wallet_id: str,
                      context: Optional[Any] = None,
                      ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).child(wallet_id).delete()

            return data

        except:

            return None

    def delete_wallet_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).child(wallet_id).child(attribute).delete()

            return data

        except:
            return None

    def get_all_wallets(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).get()

            return data

        except:
            return None
