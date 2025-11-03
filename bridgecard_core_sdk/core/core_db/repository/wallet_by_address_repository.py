
from contextlib import AbstractContextManager
from typing import Any, Callable, List, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

WALLET_BY_ADDRESS_MODEL_NAME = "wallets_by_address"


class WalletByAddressRepository(BaseRepository):

    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(
                WALLET_BY_ADDRESS_MODEL_NAME, db_session.wallets_db_app)

            self.db_ref = db_ref

    def set_data(
        self,
        address: str,
        data: dict,
    ):
        try:
            data = self.db_ref.child(address).set(data)
            return True
        except:
            return False


    def get_child_node_value(
        self,
        address: str,
    ):
        try:
            data = self.db_ref.child(address).get()
            return data
        except:
            return None

    
