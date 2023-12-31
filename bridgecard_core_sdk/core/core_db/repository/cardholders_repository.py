from contextlib import AbstractContextManager
from typing import Callable
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

CARDHOLDERS_MODEL_NAME = "cardholders"

NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME = "naira_virtual_account"


class CardholdersRepository(BaseRepository):
    
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(CARDHOLDERS_MODEL_NAME, db_session.cardholders_db_app)

            self.db_ref = db_ref

    def fetch_cardholder_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        context,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).child(attribute).get()
                
            return data

        except:
            return None

    def fetch_cardholder_data_naira_virtual_account_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        context,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).child(NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME).child(attribute).get()
                
            return data

        except:

            return None

    def update_cardholder_data_naira_virtual_account_attr_as_a_transaction(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        value,
        context,
    ):
        try:

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).child(NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME).child(attribute).transaction(
                    lambda current_value: (current_value or 0) + int(value)
                )
                
            return True

        except:

            return CARDHOLDER_DATA_UPDATE_ERROR_MESSAGE
        

    
    def update_cardholder_data_naira_virtual_account_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        value,
        context,
    ):
        try:

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).child(NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME).child(attribute).set(value)
                
            return True

        except:
            return CARDHOLDER_DATA_UPDATE_ERROR_MESSAGE

    
    


    