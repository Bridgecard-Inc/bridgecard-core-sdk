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

class CoreDbInitData(BaseModel):
    admin_db: Optional[bool] = False
    billing_db: Optional[bool] = False
    cards_db: Optional[bool] = False
    card_transactions_db: Optional[bool] = False
    cardholders_db: Optional[bool] = False
    naira_accounts_db: Optional[bool] = False


class EnvironmentEnum(str, Enum):
    sandbox = "sandbox"
    production = "production"
