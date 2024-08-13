from contextlib import AbstractContextManager
from typing import Any, Callable, List, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

WALLET_POOL_MODEL_NAME = "crypto_wallet_pool"


class WalletPoolRepository(BaseRepository):

    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(
                WALLET_POOL_MODEL_NAME, db_session.wallets_db_app)

            self.db_ref = db_ref

    def set(
        self,
        id: str,
        data: dict,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(id).set(data)
            return True
        except:
            return False

    def set_child_node(
        self,
        id: str,
        field: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(id).child(field).set(value)
            return True
        except:
            return False

    def get_child_node_value(
        self,
        id: str,
        field: str,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(id).child(field).get()
            return data
        except:
            return False

    def delete_child_node(
        self,
        id: str,
        field: str,
        context: Optional[Any] = None,
    ):
        try:
            data = self.db_ref.child(id).child(field).delete()
            return True
        except:
            return False
