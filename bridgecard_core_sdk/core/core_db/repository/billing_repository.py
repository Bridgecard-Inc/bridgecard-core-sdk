from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable
from firebase_admin import db
from ..schema.base_schema import DbSession
from .base_repository import BaseRepository


BILLING_REVENUE_DATA_MODEL_NAME = "billing_revenue_data"


class BillingRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        with db_session_factory() as db_session:

            db_ref = db.reference(BILLING_REVENUE_DATA_MODEL_NAME, db_session.billing_db_app)

            self.db_ref = db_ref


    def add_billing_revenue_data_attr_as_a_transaction(
        self,
        product_name: str,
        company_issuing_app_id: str,
        attribute: str,
        value,
        context,
    ):
        try:

            now = datetime.now()

            month_year = f"{now.month}-{now.year}"

            self.db_ref.child(product_name).child(company_issuing_app_id).child(month_year).child(attribute).transaction(
                    lambda current_value: (current_value or 0) + int(value)
                )
                
            return True

        except:
            return False
    
