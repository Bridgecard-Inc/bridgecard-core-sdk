from contextlib import AbstractContextManager
from typing import Any, Callable, List, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

COMAPNIES_MODEL_NAME = "companies"

ACCOUNTS_MODEL_NAME = "accounts"


class CompanyRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(COMAPNIES_MODEL_NAME,
                                  db_session.cardholders_db_app)

            self.db_ref = db_ref

    def fetch_all_company_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        page: int,
        keys_list: List[str],
        base_url: str,
        sort_key: Optional[str] = None,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id).child(
                    environment.value).get()
            )

            companies_data, meta = self.paginate_data(
                page=page,
                keys_list=keys_list,
                base_url=base_url,
                sort_key=sort_key,
                data=data,
                url_path="",
                environment=environment,
            )

            return companies_data, meta

        except:
            return None

    def fetch_company_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_id: str,
        context: Optional[Any] = None,
    ):
        # try:
        data = (
            self.db_ref.child(company_issuing_app_id)
            .child(environment.value)
            .child(company_id)
            .get()
        )

        print(company_issuing_app_id,environment.value,company_id,data)

        return data

        # except:
        #     return None

    def add_company_account_info(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_id: str,
        account_id: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                company_id).child(ACCOUNTS_MODEL_NAME).child(account_id).set(value)

            return True

        except:

            return None

    def set_company_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(company_id)
                .set(value)
            )

            return True

        except:
            return None

    def fetch_company_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:
            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(company_id)
                .child(attribute)
                .get()
            )

            return data

        except:
            return None

    def set_company_child_atrr_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_id: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(company_id)
                .child(child_atrr)
                .set(value)
            )

            return True

        except:
            return None

    def delete_company(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_id: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:
            (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(company_id)
                .delete()
            )

            return True

        except:
            return None

    def delete_company_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:
            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                company_id
            ).child(attribute).delete()

            return True

        except:
            return None

    def fetch_company_data_by_name(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_name: str,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(company_issuing_app_id).child(
                environment.value).order_by_child("company_name").equal_to(company_name).get()
            if not data:
                return None
            dict_key = list(data.keys())[0]
            company = data[dict_key]
            if "company_id" not in company:
                company["company_id"] = dict_key
            return company

        except:
            return None

    def set_company_card_or_wallet_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        company_id: str,
        attribute: str,
        value_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                company_id).child(attribute).child(value_id).set(value)

            return data
        except:
            return None
