from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class DbSession(BaseModel):
    admin_db_app: Any
    billing_db_app: Any
    cards_db_app: Any
    card_transactions_db_app: Any
    cardholders_db_app: Any
    naira_accounts_db_app: Any
    accounts_db_app: Any
    client_logs_db_app: Any
    cache_db_client: Any
    test_service_db_app: Any
    wallets_db_app: Any


class CoreDbInitData(BaseModel):
    admin_db: Optional[bool] = False
    billing_db: Optional[bool] = False
    cards_db: Optional[bool] = False
    card_transactions_db: Optional[bool] = False
    cardholders_db: Optional[bool] = False
    wallets_db: Optional[bool] = False
    naira_accounts_db: Optional[bool] = False
    accounts_db: Optional[bool] = False
    cache_db: Optional[bool] = False
    client_logs_db: Optional[bool] = False
    test_service_db: Optional[bool] = False


class EnvironmentEnum(str, Enum):
    sandbox = "sandbox"
    production = "production"


class Pagination(BaseModel):
    total: int
    pages: int
