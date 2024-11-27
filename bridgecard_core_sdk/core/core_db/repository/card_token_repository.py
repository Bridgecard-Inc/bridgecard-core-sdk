from contextlib import AbstractContextManager
import json
from typing import Any, Callable, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db
from bridgecard_core_sdk.core.core_auth.core_auth import ISSUNG_PRODUCT_GROUP


CARD_TOKEN_NAME = "card_token_db"


class CardTokenRepository(BaseRepository):

    def __init__(
        self,
        db_session_factory: Callable[..., AbstractContextManager[DbSession]],
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(CARD_TOKEN_NAME, db_session.cards_db_app)

            self.db_ref = db_ref
