from contextlib import AbstractContextManager
from typing import Any, Callable, List, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db


NAIRA_BANK_ACCOUNT_MAPPING_MODEL_NAME = "naira_bank_account_mapping"


class NairaBankAccountMappingRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(
                NAIRA_BANK_ACCOUNT_MAPPING_MODEL_NAME, db_session.naira_accounts_db_app
            )

            self.db_ref = db_ref

    def set_naira_account_mapping_child_atrr_data(
        self,
        bank_account_number: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(bank_account_number).child(child_atrr).set(value)

            return data

        except:

            return None

    def fetch_naira_account_mapping_data_attr(
        self,
        bank_account_number: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(bank_account_number).child(attribute).get()

            return data

        except:
            return None

    def filter_naira_account_mapping_data_by_attr(
        self,
        attribute: str,
        attribute_value: str,
        context: Optional[Any] = None,
    ):
        try:

            ordered_dict_data = (
                self.db_ref.order_by_child(attribute).equal_to(attribute_value).get()
            )

            dict_data = dict(ordered_dict_data)

            if ordered_dict_data is None:

                return []

            elif dict_data == {}:

                return []

            return list(dict_data.values())

        except:
            
            return None
