from contextlib import AbstractContextManager
from datetime import datetime
import time
from typing import Any, Callable, Dict, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

CLIENT_REQUESTS_MODEL_NAME = "client_requests"

NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME = "naira_virtual_account"

ACCOUNTS_MODEL_NAME = "accounts"

class ClientRequestsRepository(BaseRepository):

    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(CLIENT_REQUESTS_MODEL_NAME,
                                  db_session.client_logs_db_app)

            self.db_ref = db_ref

    def save_client_logs_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        client_log: Dict[str, Any],
        context: Optional[Any] = None,
    ):
        try:

            req_id = time.time_ns()
            today = datetime.today().strftime("%Y-%m-%d")
            self.db_ref.child(company_issuing_app_id).child(today).child(
                str(req_id)
            ).set(client_log)

            return True

        except:

            return None