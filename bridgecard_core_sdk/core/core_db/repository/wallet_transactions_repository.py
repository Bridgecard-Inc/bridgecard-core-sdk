from contextlib import AbstractContextManager
from typing import Any, Callable, List, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db

WALLET_TRANSACTIONS_MODEL_NAME = "wallet_transactions"


class WalletTransactionsRepository(BaseRepository):
    
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(WALLET_TRANSACTIONS_MODEL_NAME, db_session.wallets_db_app)

            self.db_ref = db_ref

    def fetch_wallet_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        transaction_reference: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(wallet_id).child(transaction_reference).get()
                
            return data

        except:
            
            return None

        
    def set_wallet_transaction_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        transaction_reference: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            prev_data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(wallet_id).child(transaction_reference).get()

            if not prev_data:

                prev_data = {}

            updated_data = {**value, **prev_data}

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(wallet_id).child(transaction_reference).update(updated_data)
                
            return prev_data

        except:
            
            return None

    def fetch_wallet_transaction_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        attribute: str,
        transaction_reference: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(wallet_id).child(transaction_reference).child(attribute).get()
                
            return data

        except:
            return None

    

    def set_wallet_transaction_child_atrr_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        child_atrr: str,
        transaction_reference: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(wallet_id).child(transaction_reference).child(child_atrr).set(value)
                
            return data

        except:
            
            return None

    
    def delete_wallet_transaction(self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        transaction_reference: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(wallet_id).child(transaction_reference).delete()
                
            return data

        except:
            
            return None


    def delete_wallet_transaction_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        transaction_reference: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(wallet_id).child(transaction_reference).child(attribute).delete()
                
            return data

        except:
            return None


    def fetch_all_wallet_transactions_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        wallet_id: str,
        page: int,
        keys_list: List[str],
        base_url: str,
        sort_key: Optional[str] = None,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(company_issuing_app_id).child(environment.value).child(wallet_id).get()

            wallet_transaction_data, meta = self.paginate_data(
                page=page,
                keys_list=keys_list,
                base_url=base_url,
                sort_key=sort_key,
                data=data,
                url_path="",
                environment=environment,
            )

            return wallet_transaction_data, meta

        except:
            return None, None