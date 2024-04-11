from contextlib import AbstractContextManager
from typing import Callable

from bridgecard_core_sdk.core.core_auth.core_auth import CoreAuth
from ..core_db import DbSession
from .base_repository import BaseRepository
from typing import Any, Callable, Optional


ADMINISTRATORS_MODEL_NAME = "administrators"


class AdminRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):

        super().__init__(db_session_factory, ADMINISTRATORS_MODEL_NAME)

        self.auth = CoreAuth(
            admin_repo=self,
        )


    def update_admin_attr(
        self,
        field: str,
        id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            self.db_ref.child(id).child(field).update(value)
                
            return True

        except:
            return None
    