from contextlib import AbstractContextManager
from typing import Any, Callable, List, Optional
from ..core_db import DbSession
from .base_repository import BaseRepository
from ..schema.base_schema import EnvironmentEnum
from firebase_admin import db


TEST_CASE_SERVICE = "test_service_db"


class TestServiceRepo(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:
            db_ref = db.reference(TEST_CASE_SERVICE, db_session.test_service_db_app)

            self.db_ref = db_ref

    def set_test_group_data(
        self,
        tag: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(tag).child(child_atrr).set(value)

            return data

        except:

            return None

    def set_test_case_data(
        self,
        tag: str,
        group: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:

            data = self.db_ref.child(tag).child(group).child(child_atrr).set(value)

            return data

        except:

            return None

    def test_group_filter_db(
        self,
        tag: str,
        child_atrr: str,
        value,
        context: Optional[Any] = None,
    ):
        try:
            ordered_dict_data = (
                self.db_ref.child(tag).order_by_child(child_atrr).equal_to(value).get()
            )

            dict_data = dict(ordered_dict_data)

            if ordered_dict_data is None:
                return None

            elif dict_data == {}:
                return None

            dict_key = list(dict_data.keys())[0]

            return dict_data[dict_key]

        except:
            return None
