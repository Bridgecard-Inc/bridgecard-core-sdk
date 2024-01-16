from typing import Optional

from pydantic import BaseModel

from .core.core_db.core_db import CoreDbInitData, init_core_db
from .issuing.billing_service.billing_service import init_billing_service
from .issuing.transaction_monitoring_service.transaction_monitoring_service import init_transaction_monitoring_service
from .core.core_auth.core_auth import init_core_auth


def init(
    billing_service: Optional[bool] = False,
    billing_service_init_data: Optional[bool] = False,
    core_db: Optional[bool] = False,
    core_auth: Optional[bool] = False,
    core_db_init_data: Optional[CoreDbInitData] = None,
    transaction_monitoring_service: Optional[bool] = False,
):
    if billing_service:
        init_billing_service()

    if core_db:
        init_core_db(core_db_init_data=core_db_init_data)

    if transaction_monitoring_service:

        init_transaction_monitoring_service()

    if core_auth:

        init_core_auth()
