from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

BC_GB_INTERNAL_SANDBOX_DATA_MODEL_NAME = "bc_gb_internal_sandbox_data"



class BcGbInternalSandboxRepository(BaseRepository):
    
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(BC_GB_INTERNAL_SANDBOX_DATA_MODEL_NAME, db_session.accounts_db_app)

            self.db_ref = db_ref