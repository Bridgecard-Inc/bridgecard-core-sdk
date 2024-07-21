from contextlib import AbstractContextManager
from typing import Any, Callable, List, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db


BUSINESS_ACCOUNT_TRANSACTIONS_MODEL_NAME = "business_account_transactions"


class BusinessAccountsTransactionsRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(BUSINESS_ACCOUNT_TRANSACTIONS_MODEL_NAME, db_session.accounts_db_app)

            self.db_ref = db_ref

    def fetch_business_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .get()
            )

            return True

        except:
            return None

    def fetch_all_business_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        page: int,
        keys_list: List[str],
        base_url: str,
        sort_key: Optional[str] = None,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .get()
            )

            business_account_transaction_data, meta = self.paginate_data(
                page=page,
                keys_list=keys_list,
                base_url=base_url,
                sort_key=sort_key,
                data=data,
                url_path="",
                environment=environment,
            )

            return business_account_transaction_data, meta

        except:
            return None, None

    def paginate_all_business_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        page: int,
        keys_list: List[str],
        base_url: str,
        sort_key: Optional[str] = None,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .get()
            )

            business_account_transaction_data, meta = self.paginate_data(
                page=page,
                keys_list=keys_list,
                base_url=base_url,
                sort_key=sort_key,
                data=data,
                url_path="",
                environment=environment,
            )

            return business_account_transaction_data, meta

        except:
            return None

    def set_business_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .set(value)
            )

            return True

        except:
            return None

    def upddate_business_account_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .update(value)
            )

            return True

        except:
            return None

    def fetch_business_account_transaction_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .child(attribute)
                .get()
            )

            return data

        except:
            return None

    def set_business_account_transaction_child_atrr_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .child(child_atrr)
                .set(value)
            )

            return True

        except:
            return None

    def delete_business_account(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .delete()
            )

            return True

        except:
            return None

    def delete_business_account_transaction_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        business_account_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(business_account_id)
                .child(attribute)
                .delete()
            )

            return True

        except:
            return None

    def business_accounts_filter_db(
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
