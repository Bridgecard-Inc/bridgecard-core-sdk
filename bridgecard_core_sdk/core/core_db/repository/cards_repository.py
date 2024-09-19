from contextlib import AbstractContextManager
import json
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db
from bridgecard_core_sdk.core.core_auth.core_auth import ISSUNG_PRODUCT_GROUP


CARDS_MODEL_NAME = "cards"


class CardsRepository(BaseRepository):

    def __init__(
        self, 
        db_session_factory: Callable[..., AbstractContextManager[DbSession]],
        cache_client: Optional[Any] = None,
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(CARDS_MODEL_NAME, db_session.cards_db_app)

            self.db_ref = db_ref
            
            self.cache_client = cache_client

    def fetch_card_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        context: Optional[Any] = None,
        latest: Optional[Any] = False,
    ):
        try:
            key = f"core_db_cache:{ISSUNG_PRODUCT_GROUP}:fetch_card_data:{company_issuing_app_id}:{environment.value}:{card_id}"
            if not latest and self.cache_client:
                card_data = self.cache_client.get(key=key, context=None)
                if not card_data:
                    data = (
                        self.db_ref.child(company_issuing_app_id)
                        .child(environment.value)
                        .child(card_id)
                        .get()
                    )
                    if data:
                        card_data = data
                        self.cache_client.set(
                            key=key, value=json.dumps(card_data), context=None
                        )
                        return data
                    else:
                        return None
                else:
                    card_data = json.loads(card_data)
                    card_db_ref = self.db_ref.child(company_issuing_app_id).child(environment.value).child(card_id)
                    is_active = card_db_ref.child("is_active").get()
                    is_deleted = card_db_ref.child("is_deleted").get()
                    balance_held = card_db_ref.child("balance_held").get()
                    blocked_due_to_fraud = card_db_ref.child("blocked_due_to_fraud").get()
                    maintenance_fee_held = card_db_ref.child("maintenance_fee_held").get()
                    maintenance_fee_last_charged_at = card_db_ref.child("maintenance_fee_last_charged_at").get()
                    has_done_debit_in_a_month = card_db_ref.child("has_done_debit_in_a_month").get()
                    insufficient_funds_decline_count = card_db_ref.child("insufficient_funds_decline_count").get()
                    card_provider = card_db_ref.child("card_provider").get()
                    paycaddy_card_id = card_db_ref.child("paycaddy_card_id").get()
                    paycaddy_wallet_id = card_db_ref.child("paycaddy_wallet_id").get()
                    card_number = card_db_ref.child("card_number").get()
                    brand = card_db_ref.child("brand").get()
                    card_data["is_active"] = is_active
                    card_data["is_deleted"] = is_deleted
                    card_data["balance_held"] = balance_held
                    card_data["blocked_due_to_fraud"] = blocked_due_to_fraud
                    card_data["maintenance_fee_held"] = maintenance_fee_held
                    card_data["maintenance_fee_last_charged_at"] = maintenance_fee_last_charged_at
                    card_data["has_done_debit_in_a_month"] = has_done_debit_in_a_month
                    card_data["insufficient_funds_decline_count"] = insufficient_funds_decline_count
                    card_data["card_provider"] = card_provider
                    card_data["brand"] = brand
                    card_data["paycaddy_card_id"] = paycaddy_card_id
                    card_data["paycaddy_wallet_id"] = paycaddy_wallet_id
                    card_data["card_number"] = card_number
                return card_data
            else:
                data = (
                    self.db_ref.child(company_issuing_app_id)
                    .child(environment.value)
                    .child(card_id)
                    .get()
                )
                if data and self.cache_client:
                    card_data = data
                    self.cache_client.set(
                        key=key, value=json.dumps(card_data), context=None
                    )
                return data
        except:
            return None
            

    def delete_card_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        context: Optional[Any] = None,
    ):
        try:

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(card_id)
                .delete()
            )

            return data

        except:

            return None

    def update_card_data_attr_as_a_transaction(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        attribute: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                card_id
            ).child(attribute).transaction(
                lambda current_value: (current_value or 0) + int(value)
            )

            return True

        except:
            return False

    def update_card_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        attribute: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                card_id
            ).child(attribute).set(value)

            return True

        except:
            return False

    def fetch_card_data_attr(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        attribute: str,
        context: Optional[Any] = None,
    ):
        try:

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(card_id)
                .child(attribute)
                .get()
            )

            return data

        except:

            return None

    def set_card_child_atrr_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(card_id)
                .child(child_atrr)
                .set(value)
            )

            return data

        except:

            return None

    def set_card_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        card_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(card_id)
                .set(value)
            )

            return data

        except:

            return None
