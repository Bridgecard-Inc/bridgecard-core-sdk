from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

COMAPNIES_KYC_REQUESTS_MODEL_NAME = "companies_kyc_requests"


class CompanyKycRequestRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(COMAPNIES_KYC_REQUESTS_MODEL_NAME, db_session.cardholders_db_app)

            self.db_ref = db_ref

