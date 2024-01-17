from contextlib import AbstractContextManager
from typing import Callable
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

CARDHOLDERS_MODEL_NAME = "blacklisted_cardholders"



class CardholdersRepository(BaseRepository):
    
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(CARDHOLDERS_MODEL_NAME, db_session.cardholders_db_app)

            self.db_ref = db_ref

    def fetch_blacklisted_cardholder_data_by_attribute(
        self,
        attribute: str,
        value: str,
        context,
    ):
        try:

            data = self.db_ref.child(attribute).child(value).get()
                
            return data

        except:
            
            return None
