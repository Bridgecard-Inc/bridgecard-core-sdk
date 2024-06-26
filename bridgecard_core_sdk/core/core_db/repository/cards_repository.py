from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db


CARDS_MODEL_NAME = "cards"


class CardsRepository(BaseRepository):

    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(CARDS_MODEL_NAME, db_session.cards_db_app)

            self.db_ref = db_ref

    def fetch_card_data(
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
                .get()
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
