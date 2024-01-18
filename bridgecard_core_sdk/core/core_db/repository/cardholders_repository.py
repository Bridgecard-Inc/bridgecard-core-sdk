from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
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

    def fetch_cardholder_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).get()
                
            return data

        except:
            
            return None
        
    def set_cardholder_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).set(value)
                
            return data

        except:
            
            return None

    def fetch_cardholder_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        context: Optional[Any] = None,
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
        context: Optional[Any] = None,
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
        context: Optional[Any] = None,
    ):
        try:

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).child(NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME).child(attribute).transaction(
                    lambda current_value: (current_value or 0) + int(value)
                )
                
            return True

        except:

            return None
        

    
    def update_cardholder_data_naira_virtual_account_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).child(NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME).child(attribute).set(value)
                
            return True

        except:
            return None
    

    def set_cardholder_child_atrr_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).child(child_atrr).set(value)
                
            return data

        except:
            
            return None

    
    def cardholder_order_by_child(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        child_atrr: str,
        value:str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).order_by_child(child_atrr).equal_to(value).get()
                
            return data

        except:
            
            return None

    
    def delete_cardholder(self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        value:str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).delete()
                
            return data

        except:
            
            return None


    def delete_cardholder_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(cardholder_id).child(attribute).delete()
                
            return data

        except:
            return None
