from contextlib import AbstractContextManager, contextmanager
from datetime import datetime
import time
from redis import Redis
import os
from typing import Any, Callable, Optional
from fastapi import Header

from starlette.requests import Request

from bridgecard_core_sdk.core.core_auth.error import (
    InvalidToken,
    AuthenticationTokenMismatch,
    IssuingPermissionHasBeenDeactivated,
)
from bridgecard_core_sdk.core.core_auth.schema.base_schema import ProvidersEnum
# from bridgecard_core_sdk.core.core_db.core_db import CoreDbUsecase

from bridgecard_core_sdk.core.core_db.schema.base_schema import EnvironmentEnum
from bridgecard_core_sdk.core.utils.rest_api_client.rest_api_client import RestApiClient

from bridgecard_core_sdk.core.core_db.utils.core_db_data_context import (
    core_db_data_context,
)


PREFIX = "Bearer"
test_authorization_token_prefix = "at_test_"
test_secret_key_prefix = "sk_test_"
live_authorization_token_prefix = "at_live_"
live_secret_key_prefix = "sk_live_"


ISSUNG_PRODUCT_GROUP = "issuing"


class CoreAuth:
    def __init__(self, admin_repo):
        self.admin_repo = admin_repo

    async def verify_token(
        self, token: Optional[str] = Header(None), request: Request = None
    ):
        request_time = int(time.time())

        if token is None:
            return InvalidToken
        if not token.startswith(PREFIX):
            return InvalidToken

        if request is None:
            return AuthenticationTokenMismatch
        req = request.url.path

        if "sandbox" in req and "at_live" in token:
            return AuthenticationTokenMismatch

        if "sandbox" not in req and "at_test" in token:
            return AuthenticationTokenMismatch

        if "sandbox" in req:
            environment = EnvironmentEnum.sandbox
        else:
            environment = EnvironmentEnum.production

        token = token[len(PREFIX):].lstrip()
        filter_string = "live_authorization_token"
        if token.startswith(test_authorization_token_prefix):
            filter_string = "test_authorization_token"

        data = self.admin_repo.filter_db(filter_string, token, None)

        if data == None:
            return InvalidToken

        data["token"] = token
        data["environment"] = environment

        if "sandbox" in req:
            if "sandbox_webhook_url" in list(data.keys()):
                data["webhook_url"] = data["sandbox_webhook_url"]

        if "webhook_url" not in list(data.keys()):
            data["webhook_url"] = "https://google.com"

        client_details = data

        if (
            client_details["is_account_verified"] == False
            and client_details["environment"] == EnvironmentEnum.production
        ):
            return IssuingPermissionHasBeenDeactivated

        client_details["headers"] = dict(request.headers.items())
        client_details["request_time"] = request_time
        client_details["endpoint_url"] = str(request.url)

        return client_details

    def get_client_from_issuing_id(
        self, issuing_app_id: str, environment: EnvironmentEnum
    ):
        request_time = int(time.time())

        data = self.admin_repo.filter_db(
            "issuing_app_id", issuing_app_id, None)

        if data == None:
            raise InvalidToken

        if environment == EnvironmentEnum.production:
            data["token"] = data["live_authorization_token"]
        else:
            data["token"] = data["test_authorization_token"]

        data["environment"] = environment

        client_details = data

        if (
            client_details["is_account_verified"] == False
            and client_details["environment"] == EnvironmentEnum.production
        ):
            if "test_card" not in list(data.keys()):
                raise IssuingPermissionHasBeenDeactivated

        client_details["headers"] = {}
        client_details["request_time"] = request_time
        client_details["endpoint_url"] = ""

        return client_details

    def parse_auth_token_from_header(header: str):
        if header is None:
            raise InvalidToken
        if not header.startswith(PREFIX):
            raise InvalidToken

        return header[len(PREFIX):].lstrip()


def fetch_provider_token(provider: str, environment: EnvironmentEnum, login_url: str):

    delimiter = "-----"

    core_db_usecase = core_db_data_context.core_db_usecase

    if provider == ProvidersEnum.bopayments_module_visa:
        if environment == EnvironmentEnum.production:
            username = os.environ.get("BOPAYMENTS_LIVE_USERNAME")

            password = os.environ.get("BOPAYMENTS_LIVE_PASSWORD")

            api_key = os.environ.get("BOPAYMENTS_LIVE_APIKEY")

        else:
            username = os.environ.get("BOPAYMENTS_TEST_USERNAME")

            password = os.environ.get("BOPAYMENTS_TEST_PASSWORD")

            api_key = os.environ.get("BOPAYMENTS_TEST_APIKEY")

        jwt_token_key = f"core_monitoring:{ISSUNG_PRODUCT_GROUP}:{provider}:jwt_token"

        jwt_token = core_db_usecase.cache_repository.get(
            key=jwt_token_key, context=None
        )

        if (
            jwt_token
            and int(datetime.timestamp(datetime.now())) <= int(jwt_token.split(delimiter)[1])
        ):

            return jwt_token.split(delimiter)[0]

        else:

            payload = {"email": username, "password": password}

            headers = {"Content-Type": "application/json", "ApiKey": api_key}

            rest_api_client = RestApiClient(headers=headers)

            response_status_code, response_dict = rest_api_client.post(
                url=login_url,
                data=payload,
            )

            if response_status_code == 200:

                auth_token = response_dict["auth_token"]

                expires = int(datetime.timestamp(datetime.now())) + 1700

                jwt_token = f"{auth_token}{delimiter}{expires}"

                res = core_db_usecase.cache_repository.set(
                    key=jwt_token_key, value=jwt_token, context=None
                )

                return auth_token

            else:

                return False


def init_core_auth():
    ...
