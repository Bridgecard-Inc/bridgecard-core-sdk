from contextlib import AbstractContextManager, contextmanager
from redis import Redis
import os
from typing import Any, Callable, Optional
import firebase_admin
from firebase_admin import db, credentials
from .schema.base_schema import CoreDbInitData, DbSession
from .utils.methods import decode_base_64_to_json
from pydantic import BaseModel
from .repository import (
    CardsRepository,
    AdminRepository,
    BillingRepository,
    CardholdersRepository,
    CardTransactionsRepository,
    NairaAccountsRepository,
    CacheRepository,
    ManuallyPassedKycLogsRepository,
    BlackListedCardholdersRepository,
    CompanyRepository,
    CompanyKycRequestRepository
)

from .utils.core_db_data_context import core_db_data_context


class CoreDbUsecase:
    def __init__(
        self,
        cards_repository: Optional[CardsRepository] = None,
        admin_repository: Optional[AdminRepository] = None,
        cardholders_repository: Optional[CardholdersRepository] = None,
        company_repository: Optional[CompanyRepository] = None,
        company_kyc_request_repository: Optional[CompanyKycRequestRepository] = None,
        blacklisted_cardholders_repository: Optional[BlackListedCardholdersRepository] = None,
        card_transactions_repository: Optional[CardTransactionsRepository] = None,
        naira_accounts_repository: Optional[NairaAccountsRepository] = False,
        billing_repository: Optional[AdminRepository] = None,
        cache_repository: Optional[CacheRepository] = None,
        manually_passed_kyc_logs_repository: Optional[
            ManuallyPassedKycLogsRepository
        ] = None,
    ):
        self.cards_repository = cards_repository
        self.admin_repository = admin_repository
        self.cardholders_repository = cardholders_repository
        self.company_repository = company_repository
        self.company_kyc_request_repository = company_kyc_request_repository
        self.card_transactions_repository = card_transactions_repository
        self.naira_accounts_repository = naira_accounts_repository
        self.billing_repository = billing_repository
        self.cache_repository = cache_repository
        self.blacklisted_cardholders_repository = blacklisted_cardholders_repository
        self.manually_passed_kyc_logs_repository = manually_passed_kyc_logs_repository


class Database:
    def __init__(self, core_db_init_data: Optional[CoreDbInitData] = None) -> None:
        google_config_base64 = os.environ.get("GOOGLE_CONFIG_BASE64")

        database_url = os.environ.get("DATABASE_URL")

        storage_bucket_url = os.environ.get("STORAGE_BUCKET_URL")

        self._cred = credentials.Certificate(
            decode_base_64_to_json(google_config_base64)
        )

        self._firebase_app = firebase_admin.initialize_app(
            self._cred,
            {
                "databaseURL": database_url,
                "storageBucket": storage_bucket_url,
            },
        )

        self._admin_db_app = None

        if core_db_init_data.admin_db:
            admin_database_url = os.environ.get("ADMIN_DATABASE_URL")

            self._admin_db_app = firebase_admin.initialize_app(
                self._cred,
                {"databaseURL": admin_database_url},
                name="admin_db_app",
            )

        self._billing_db_app = None

        if core_db_init_data.billing_db:
            billing_database_url = os.environ.get("BILLING_DATABASE_URL")

            self._billing_db_app = firebase_admin.initialize_app(
                self._cred,
                {"databaseURL": billing_database_url},
                name="billing_db_app",
            )

        self._cards_db_app = None

        if core_db_init_data.cards_db:
            cards_database_url = os.environ.get("CARDS_DATABASE_URL")

            self._cards_db_app = firebase_admin.initialize_app(
                self._cred,
                {"databaseURL": cards_database_url},
                name="cards_db_app",
            )

        self._card_transactions_db_app = None

        if core_db_init_data.card_transactions_db:
            card_transactions_database_url = os.environ.get(
                "CARD_TRANSACTIONS_DATABASE_URL"
            )

            self._card_transactions_db_app = firebase_admin.initialize_app(
                self._cred,
                {"databaseURL": card_transactions_database_url},
                name="card_transactions_db_app",
            )

        self._cardholders_db_app = None

        if core_db_init_data.cardholders_db:
            cardholders_database_url = os.environ.get("CARDHOLDERS_DATABASE_URL")

            self._cardholders_db_app = firebase_admin.initialize_app(
                self._cred,
                {"databaseURL": cardholders_database_url},
                name="cardholders_db_app",
            )

        self._naira_accounts_db_app = None

        if core_db_init_data.naira_accounts_db:
            naira_accounts_database_url = os.environ.get("NAIRA_ACCOUNTS_DATABASE_URL")

            self._naira_accounts_db_app = firebase_admin.initialize_app(
                self._cred,
                {"databaseURL": naira_accounts_database_url},
                name="naira_account_db_app",
            )

        self.client_log_db_app = None

        if core_db_init_data.client_logs_db:
            client_logs_database_url = os.environ.get("CLIENT_LOGS_DATABASE_URL")

            self.client_log_db_app = firebase_admin.initialize_app(
                self._cred,
                {"databaseURL": client_logs_database_url},
                name="client_log_db_app",
            )

        self.cache_db_client = None

        if core_db_init_data.cache_db:
            redis_host = os.environ.get("REDIS_HOST")

            redis_port = os.environ.get("REDIS_PORT")

            redis_username = os.environ.get("REDIS_USERNAME")

            redis_password = os.environ.get("REDIS_PASSWORD")

            redis = Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
                username=redis_username,
                password=redis_password,
            )

            if redis.ping():
                self.cache_db_client = redis
            else:
                print("Failed to Redis")

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[DbSession]]:
        db_session = DbSession(
            admin_db_app=self._admin_db_app,
            billing_db_app=self._billing_db_app,
            cards_db_app=self._cards_db_app,
            card_transactions_db_app=self._card_transactions_db_app,
            cardholders_db_app=self._cardholders_db_app,
            naira_accounts_db_app=self._naira_accounts_db_app,
            cache_db_client=self.cache_db_client,
            client_logs_db_app=self.client_log_db_app,
        )
        try:
            yield db_session
        except Exception:
            # Handle exceptions and cleanup if needed
            raise
        finally:
            # Perform cleanup actions here if needed
            ...


def init_core_db(core_db_init_data: Optional[CoreDbInitData] = None):
    
    db = Database(core_db_init_data)

    cards_repository = CardsRepository(db_session_factory=db.session)

    card_transactions_repository = CardTransactionsRepository(
        db_session_factory=db.session
    )

    cardholders_repository = None
    blacklisted_cardholders_repository = None
    company_repository = None
    company_kyc_request_repository = None

    if core_db_init_data.cardholders_db:
        cardholders_repository = CardholdersRepository(db_session_factory=db.session)
        blacklisted_cardholders_repository = BlackListedCardholdersRepository(db_session_factory=db.session)
        company_repository =  CompanyRepository(db_session_factory=db.session)
        company_kyc_request_repository = CompanyKycRequestRepository(db_session_factory=db.session)

    naira_accounts_repository = None

    if core_db_init_data.naira_accounts_db:
        naira_accounts_repository = NairaAccountsRepository(
            db_session_factory=db.session
        )

    billing_repository = None

    if core_db_init_data.billing_db:
        billing_repository = BillingRepository(db_session_factory=db.session)

    admin_repository = None

    if core_db_init_data.admin_db:
        admin_repository = AdminRepository(db_session_factory=db.session)

    cache_repository = None

    if core_db_init_data.cache_db:
        cache_repository = CacheRepository(db_session_factory=db.session)

    manually_passed_kyc_logs_repository = None

    if core_db_init_data.client_logs_db:
        manually_passed_kyc_logs_repository = ManuallyPassedKycLogsRepository(
            db_session_factory=db.session
        )

    core_db_usecase = CoreDbUsecase(
        cards_repository=cards_repository,
        card_transactions_repository=card_transactions_repository,
        cardholders_repository=cardholders_repository,
        company_repository=company_repository,
        company_kyc_request_repository=company_kyc_request_repository
        naira_accounts_repository=naira_accounts_repository,
        billing_repository=billing_repository,
        admin_repository=admin_repository,
        cache_repository=cache_repository,
        blacklisted_cardholders_repository = blacklisted_cardholders_repository,
        manually_passed_kyc_logs_repository=manually_passed_kyc_logs_repository,
    )

    core_db_data_context.core_db_usecase = core_db_usecase
