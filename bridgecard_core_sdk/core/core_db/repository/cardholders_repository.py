from contextlib import AbstractContextManager
import json
from typing import Any, Callable, Optional

from bridgecard_core_sdk.core.core_auth.core_auth import ISSUNG_PRODUCT_GROUP
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db
from bridgecard_core_sdk.core.core_db.utils.core_db_data_context import (
    core_db_data_context,
)


CARDHOLDERS_MODEL_NAME = "cardholders"

NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME = "naira_virtual_account"

ACCOUNTS_MODEL_NAME = "accounts"


class CardholdersRepository(BaseRepository):

    def __init__(
        self,
        db_session_factory: Callable[..., AbstractContextManager[DbSession]],
        cache_client: Optional[Any] = None,
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(CARDHOLDERS_MODEL_NAME, db_session.cardholders_db_app)

            self.db_ref = db_ref

            self.cache_client = cache_client

    def fetch_cardholder_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        context: Optional[Any] = None,
        latest: Optional[Any] = False,
    ):
        try:
            key = f"core_db_cache:{ISSUNG_PRODUCT_GROUP}:fetch_cardholder_data:{company_issuing_app_id}:{environment.value}:{cardholder_id}"
            if not latest and self.cache_client:
                cardholder_data = self.cache_client.get(key=key, context=None)
                if not cardholder_data:
                    data = (
                        self.db_ref.child(company_issuing_app_id)
                        .child(environment.value)
                        .child(cardholder_id)
                        .get()
                    )
                    if data:
                        cardholder_data = data.copy()
                        if "saved_identity_record" in cardholder_data:
                            cardholder_data.pop("saved_identity_record")
                        if "cards" in cardholder_data:
                            cardholder_data.pop("cards")
                        self.cache_client.set(
                            key=key, value=json.dumps(cardholder_data), context=None
                        )
                        return data
                    else:
                        return None
                else:
                    cardholder_data = json.loads(cardholder_data)
                return cardholder_data
            else:
                data = (
                    self.db_ref.child(company_issuing_app_id)
                    .child(environment.value)
                    .child(cardholder_id)
                    .get()
                )
                if data and self.cache_client:
                    cardholder_data = data.copy()
                    if "saved_identity_record" in cardholder_data:
                        cardholder_data.pop("saved_identity_record")
                    if "cards" in cardholder_data:
                        cardholder_data.pop("cards")
                    self.cache_client.set(
                        key=key, value=json.dumps(cardholder_data), context=None
                    )
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

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(cardholder_id)
                .child(NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME)
                .child(attribute)
                .get()
            )

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

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(cardholder_id)
                .set(value)
            )

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

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(cardholder_id)
                .child(attribute)
                .get()
            )

            return data

        except:
            return None

    def set_cardholder_card_or_wallet_data(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        value_id: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(cardholder_id)
                .child(attribute)
                .child(value_id)
                .set(value)
            )

            return data

        except:
            return None

    def delete_cardholder_card_or_wallet_data_attribute(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        attribute: str,
        value_id: str,
        context: Optional[Any] = None,
    ):
        try:

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(cardholder_id)
                .child(attribute)
                .child(value_id)
                .delete()
            )

            return data

        except:
            return None

    def add_cardholder_account_info(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        account_id: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                cardholder_id
            ).child(ACCOUNTS_MODEL_NAME).child(account_id).set(value)

            return True

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

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                cardholder_id
            ).child(NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME).child(attribute).transaction(
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

            self.db_ref.child(company_issuing_app_id).child(environment.value).child(
                cardholder_id
            ).child(NAIRA_VIRTUAL_ACCOUNT_MODEL_NAME).child(attribute).set(value)

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

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(cardholder_id)
                .child(child_atrr)
                .set(value)
            )

            return data

        except:

            return None

    def cardholder_order_by_child(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        child_atrr: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .order_by_child(child_atrr)
                .equal_to(value)
                .get()
            )

            return data

        except:

            return None

    def delete_cardholder(
        self,
        environment: EnvironmentEnum,
        company_issuing_app_id: str,
        cardholder_id: str,
        context: Optional[Any] = None,
    ):
        try:

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(cardholder_id)
                .delete()
            )

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

            data = (
                self.db_ref.child(company_issuing_app_id)
                .child(environment.value)
                .child(cardholder_id)
                .child(attribute)
                .delete()
            )

            return data

        except:
            return None
