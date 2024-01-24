from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db


ACCOUNTS_MODEL_NAME = "accounts"


class AccountsRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(
                ACCOUNTS_MODEL_NAME, db_session.accounts_db_app
            )

            self.db_ref = db_ref

    def fetch_account_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(account_id).get()
                
            return True

        except:
            
            return None
        
    def set_account_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(account_id).set(value)
                
            return True

        except:
            
            return None
        

    def set_account_data_as_a_transaction(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(account_id).transaction(
                    lambda current_value: (current_value or 0) + int(value)
                )
                
            return True

        except:
            
            return None


    def upddate_account_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(account_id).update(value)
                
            return True

        except:
            
            return None

    def fetch_account_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(account_id).child(attribute).get()
                
            return data

        except:
            return None

    def set_account_child_atrr_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(account_id).child(child_atrr).set(value)
                
            return True

        except:
            
            return None

    
    def delete_account(self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        value:str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(account_id).delete()
                
            return True

        except:
            
            return None


    def delete_account_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        account_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(account_id).child(attribute).delete()
                
            return True

        except:
            return None


    def accounts_filter_db(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        child_atrr: str,
        value:str,
        context: Optional[Any] = None,
    ):
        try:

            ordered_dict_data = self.db_ref.child(company_issuing_app_id).child(environment.value).order_by_child(child_atrr).equal_to(value).get()
                
            dict_data = dict(ordered_dict_data)

            if ordered_dict_data is None:

                return None

            elif dict_data == {}:

                return None

            dict_key = list(dict_data.keys())[0]

            return dict_data[dict_key]

        except:
            
            return None
