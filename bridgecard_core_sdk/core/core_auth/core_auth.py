from contextlib import AbstractContextManager, contextmanager
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

from bridgecard_core_sdk.core.core_db.schema.base_schema import EnvironmentEnum



PREFIX = "Bearer"
test_authorization_token_prefix = "at_test_"
test_secret_key_prefix = "sk_test_"
live_authorization_token_prefix = "at_live_"
live_secret_key_prefix = "sk_live_"


class CoreAuth:
    def __init__(self, admin_db_ref):

        self._admin_db_ref = admin_db_ref

    async def verify_token(
        self, token: Optional[str] = Header(None), request: Request = None
    ):
        request_time = int(time.time())

        if token is None:
            raise InvalidToken
        if not token.startswith(PREFIX):
            raise InvalidToken

        if request is None:
            raise AuthenticationTokenMismatch
        req = request.url.path

        if "sandbox" in req and "at_live" in token:
            raise AuthenticationTokenMismatch

        if "sandbox" not in req and "at_test" in token:
            raise AuthenticationTokenMismatch

        if "sandbox" in req:
            environment = EnvironmentEnum.sandbox
        else:
            environment = EnvironmentEnum.production

        token = token[len(PREFIX) :].lstrip()
        filter_string = "live_authorization_token"
        if token.startswith(test_authorization_token_prefix):
            filter_string = "test_authorization_token"
        data = self.admin_db_ref.filter_db(filter_string, token)

        if data == None:
            raise InvalidToken

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
            raise IssuingPermissionHasBeenDeactivated

        client_details["headers"] = dict(request.headers.items())
        client_details["request_time"] = request_time
        client_details["endpoint_url"] = str(request.url)

        return client_details

    def get_client_from_issuing_id(
        self, issuing_app_id: str, environment: EnvironmentEnum
    ):
        request_time = int(time.time())
        data = self.admin_db_ref.filter_db(
            "issuing_app_id", issuing_app_id
        )

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

        return header[len(PREFIX) :].lstrip()


def init_core_auth():
    ...
