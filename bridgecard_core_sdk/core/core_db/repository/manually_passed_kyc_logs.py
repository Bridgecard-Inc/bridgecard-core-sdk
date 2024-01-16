from contextlib import AbstractContextManager
from typing import Any, Callable

from ..core_db import DbSession
from .base_repository import BaseRepository

from firebase_admin import db


MANUALLY_PASSED_KYC_LOGS_MODEL_NAME = "manually_passed_kyc_logs_db"


class ManuallyPassedKycLogsRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(
                MANUALLY_PASSED_KYC_LOGS_MODEL_NAME, db_session.client_logs_db_app
            )

            self.db_ref = db_ref

    def fetch_child_data(
        self,
        child_data_key: str,
        context,
    ):
        try:

            data = self.db_ref.child(child_data_key).get()

            return data

        except:

            return None

    def fetch_child_data_atrr(
        self,
        child_data_key: str,
        child_attribute: str,
        context,
    ):
        try:
            data = self.db_ref.child(child_data_key).child(child_attribute).get()

            return data

        except:
            return None

    def set_child_data_atrr(
        self,
        child_data_key: str,
        child_attribute: str,
        child_attribute_value: Any,
        context,
    ):
        try:
            self.db_ref.child(child_data_key).child(child_attribute).set(
                child_attribute_value
            )

            return True

        except:
            return None
