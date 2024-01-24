from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

BC_GB_INTERNAL_SANDBOX_DATA_MODEL_NAME = "bc_gb_internal_sandbox_data"

ACCOUNTS_MODEL_NAME = "accounts"


class BcGbInternalSandboxRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(
                BC_GB_INTERNAL_SANDBOX_DATA_MODEL_NAME, db_session.accounts_db_app
            )

            self.db_ref = db_ref

    def create_raw(
        self,
        id: str,
        schema_dict,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(ACCOUNTS_MODEL_NAME).child(id).get()

            if data is not None:
                return False

            self.db_ref.child(ACCOUNTS_MODEL_NAME).child(id).set(schema_dict)

            return True

        except:
            return False

    def read(
        self,
        id: str,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(ACCOUNTS_MODEL_NAME).child(id).get()

            return data

        except:
            return False

    def read_attr(
        self,
        id: str,
        field: str,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(ACCOUNTS_MODEL_NAME).child(id).child(field).get()

            return data

        except:
            return False

    def update_attr(
        self,
        id: str,
        field: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(ACCOUNTS_MODEL_NAME).child(id).child(field).set(value)

            return data

        except:
            return False
