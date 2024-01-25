from contextlib import AbstractContextManager
from typing import Any, Callable, List, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db


ACCOUNTS_MODEL_NAME = "account_transactions"


class AccountsTransactionsRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(ACCOUNTS_MODEL_NAME, db_session.accounts_db_app)

            self.db_ref = db_ref

    def fetch_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(account_id)
                .get()
            )

            return True

        except:
            return None

    def fetch_all_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        page: int,
        keys_list: List[str],
        base_url: str,
        sort_key: Optional[str] = None,
        currency: Optional[str] = None,
        context: Optional[Any] = None,
    ):
        try:

            if not currency:

                data = (
                    self.db_ref.child(company_issuing_app_id)
                    .child(environment.value)
                    .child(account_id)
                    .get()
                )

            else:

                ordered_dict_data = (
                    self.db_ref.child(company_issuing_app_id)
                    .child(environment.value)
                    .child(account_id)
                    .order_by_child("currency").equal_to(currency).get()
                )

                data = dict(ordered_dict_data)


            account_transaction_data, meta = self.paginate_data(
                page=page,
                keys_list=keys_list,
                base_url=base_url,
                sort_key=sort_key,
                data=data,
                url_path="",
                environment=environment,
            )

            return account_transaction_data, meta

        except:
            
            return None

    def set_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(account_id)
                .set(value)
            )

            return True

        except:
            return None

    def upddate_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(account_id)
                .update(value)
            )

            return True

        except:
            return None

    def fetch_account_transaction_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(account_id)
                .child(attribute)
                .get()
            )

            return True

        except:
            return None

    def set_account_transaction_child_atrr_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(account_id)
                .child(child_atrr)
                .set(value)
            )

            return True

        except:
            return None

    def delete_account(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(account_id)
                .delete()
            )

            return True

        except:
            return None

    def delete_account_transaction_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(account_id)
                .child(attribute)
                .delete()
            )

            return True

        except:
            return None

    def accounts_filter_db(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        child_atrr: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:
            ordered_dict_data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .order_by_child(child_atrr)
                .equal_to(value)
                .get()
            )

            dict_data = dict(ordered_dict_data)

            if ordered_dict_data is None:
                return None

            elif dict_data == {}:
                return None

            dict_key = list(dict_data.keys())[0]

            return dict_data[dict_key]

        except:
            return None
