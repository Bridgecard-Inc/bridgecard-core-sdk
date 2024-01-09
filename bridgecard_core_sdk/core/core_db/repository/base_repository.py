from contextlib import AbstractContextManager
from typing import Callable, Optional
from firebase_admin import db
from ..core_db import DbSession


class BaseRepository:
    def __init__(
        self,
        db_session_factory: Callable[..., AbstractContextManager[DbSession]],
        model: str,
    ) -> DbSession:
        with db_session_factory() as db_session:
            db_ref = db.reference(model, db_session.admin_db_app)

            self.db_ref = db_ref

    def read_by_id(self, id: str, context):
        try:
            data = self.db_ref.child(id).get()
            return data
        except:
            return False

    def read_attr(self, id: str, field: str, context):
        try:
            data = self.db_ref.child(id).child(field).get()

            return data

        except:
            return False

    def create(self, id: str, schema, context):
        try:
            obj_in = schema.dict()

            data = self.db_ref.child(id).get()

            if data is not None:

                return False

            self.db_ref.child(id).set(obj_in)

            return True

        except:
            return False

    def update(self, id: str, schema, context):
        try:
            obj_in = schema.dict()

            self.db_ref.child(id).update(obj_in)

            return True

        except:
            return False

    def update_attr(self, id: str, field: str, value, context):
        try:
            self.db_ref.child(id).child(field).set(value)

            return True

        except:
            return False

    def update_attr_as_a_transaction(
        self,
        id: str,
        field: str,
        value,
        context,
        is_reduction: Optional[bool] = True,
    ):
        try:

            if is_reduction:

                self.db_ref.child(id).child(field).transaction(
                    lambda current_value: current_value - int(value)
                )
            
            else:

                self.db_ref.child(id).child(field).transaction(
                    lambda current_value: current_value + int(value)
                )


            return True

        except:
            return False

    def delete_by_id(self, id: str, context):
        try:
            self.db_ref.child(id).delete()

            return True

        except:
            return False

    def filter_db(self, field: str, value: str, context):
        ordered_dict_data = self.db_ref.order_by_child(field).equal_to(value).get()

        dict_data = dict(ordered_dict_data)

        if ordered_dict_data is None:
            return False

        elif dict_data == {}:
            return False

        dict_key = list(dict_data.keys())[0]

        return dict_data[dict_key]
