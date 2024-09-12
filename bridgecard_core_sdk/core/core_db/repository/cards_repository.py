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
            if not latest:
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
                return card_data
            else:
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
