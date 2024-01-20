from contextlib import AbstractContextManager
from typing import Callable, List, Optional
from firebase_admin import db

from bridgecard_core_sdk.core.core_db.schema.base_schema import EnvironmentEnum, Pagination
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
    

    def paginate_data(self, page: int, data: List[dict], keys_list: List[str], base_url: str, url_path: str, environment: EnvironmentEnum, sort_key: Optional[str] = None, is_data_already_a_list : Optional[bool] = False, ):

        if data == None:

            pagination = Pagination(total=0, pages=0, previous=None, next=None)

            data = []

            return data, pagination

        tuple_keys = tuple(keys_list)

        if not is_data_already_a_list:

            data = list(data.values())


        data = [dict((k, d.get(k, None)) for k in tuple_keys) for d in data]
        
        if sort_key:

            data = sorted(data, key=lambda i: i[f"{sort_key}"], reverse=True)

        if len(data) % 20 == 0:
            pages = len(data) / 20
        else:
            pages = int(len(data) / 20)
            pages += 1

        if environment == EnvironmentEnum.production.value:

            url = base_url + url_path
        else:
            url = base_url + url_path

        if len(data) > (page + 1) * 20 or len(data) > (page * 20):
            next_page = page + 1
            next_page = f"{url}?page={next_page}"
        else:
            next_page = None

        if page == 1:
            pagination = Pagination(
                total=len(data), pages=pages, previous=None, next=next_page
            )

            data = data[:20]

            return data, pagination

        elif len(data) > page * 20:
            previous_page = f"{url}?page={(page-1)}"

            pagination = Pagination(
                total=len(data),
                pages=pages,
                previous=previous_page,
                next=next_page,
            )

            data = data[(page - 1) * 20 : page * 20]

            return data, pagination

        elif len(data) > (page - 1) * 20:
            previous_page = f"{url}?page={(page-1)}"

            pagination = Pagination(
                total=len(data),
                pages=pages,
                previous=previous_page,
                next=None,
            )

            data = data[(page - 1) * 20 : page * 20]

            return data, pagination

        else:
            pagination = Pagination(
                total=len(data), pages=pages, previous=None, next=None
            )

            data = []

            return data, pagination
