from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
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
