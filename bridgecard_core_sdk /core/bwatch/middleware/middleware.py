"""
ASGI MIDDLEWARE
"""

import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from bwatch_python.utils.api_helper import ApiHelper
from bwatch_python.utils import constants
from ..utils.methods import data_mapper

from bwatch_python.utils.methods import fetch_usecase_rules
from .models import Rule, RuleParameterEnum, SessionProperties, EnvironmentDetails
from ..utils.bwatch_data_context import bwatch_python_data_context

from ..data.bwatch_data import create_transaction

import copy

api_helper = ApiHelper()


class BWatchAsgiMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        # some_attribute: str,
    ):
        super().__init__(app)
        # self.some_attribute = some_attribute

    async def app(self, request: Request):
        return

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(self, request: Request, call_next):

        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        query_params = dict(request.query_params)
        path_params = dict(request.path_params)
        client = {"host": request.client.host, "port": request.client.port}
        cookies = request.cookies

        try:
            await self.set_body(request)
            jsonbody = await request.json()
        except:
            jsonbody = {}

        session = SessionProperties(
            method=method,
            url=url,
            headers=headers,
            query_params=query_params,
            path_params=path_params,
            client=client,
            cookies=cookies,
            body=dict(jsonbody),
        )

        # enivronment = EnvironmentDetails(
        #     language="Python", version="", package="FASTAPI", other_details={}
        # )

        if session.url == bwatch_python_data_context.url_to_track_on_middleware:

            response = _process_as_middleware(session=session)

            if response is not None:

                return response

        response = await call_next(request)

        return response

def _process_as_middleware(session: SessionProperties):

    custom_redis_handler = CustomRedisHandler(username=bwatch_python_data_context.app_id,password=bwatch_python_data_context.secret_key)

    fraudulent_customers_dict = custom_redis_handler.fetch_fraudulent_customers_dict()

    # print(fraudulent_customers_dict)

    id_to_track_on_middleware = bwatch_python_data_context.id_to_track_on_middleware

    id_to_track_on_middleware = session.body.get(id_to_track_on_middleware)

    if id_to_track_on_middleware in fraudulent_customers_dict and fraudulent_customers_dict.get(id_to_track_on_middleware):

        session.body = {
            "message": "This user has been flagged for fruad by our system, please contact card issuer"
        }

        response = Response(
            json.dumps(session.body), media_type="application/json", status_code=403
        )

        return response

    else:

        session_copy = copy.deepcopy(session.body)

        transactions_data_mappers_copy = copy.deepcopy(
            bwatch_python_data_context.transactions_data_mappers
        )

        create_transaction(
            session_copy,
            mapping=transactions_data_mappers_copy,
        )

        result = fetch_usecase_rules(
            rules=custom_redis_handler.fetch_high_urgency_usecase_rules_dict()
        )

        usecase_rules = result.get("data")

        transaction_data_dict = data_mapper(
            data=session_copy,
            mapping=transactions_data_mappers_copy,
        )

        if usecase_rules:

            total_rules_count = len(usecase_rules)

            total_risk_score = 0

            for rule in usecase_rules:

                rule = Rule(**rule)

                rule_key_list = rule.key.split(".")

                rule_comparison_value = 0

                if rule_key_list[0] == "transactions":

                    for key_index in range(len(rule_key_list)):

                        if key_index == 0:

                            continue

                        elif key_index == 1:

                            rule_comparison_value = transaction_data_dict.get(
                                rule_key_list[key_index].lstrip().rstrip()
                            )

                        else:

                            rule_comparison_value = rule_comparison_value.get(
                                rule_key_list[key_index].lstrip().rstrip()
                            )

                    if rule.parameter == RuleParameterEnum.DATA_COMPARISON_EQUAL_TO:

                        if rule_comparison_value == rule.value:

                            total_risk_score += int(rule.risk_score)

                    elif (
                        rule.parameter == RuleParameterEnum.DATA_COMPARISON_NOT_EQUAL_TO
                    ):

                        if rule_comparison_value != rule.value:

                            total_risk_score += int(rule.risk_score)

                    elif rule.parameter == RuleParameterEnum.DATA_MATCH_GREATER_THAN:

                        if int(rule_comparison_value) > int(rule.value):

                            total_risk_score += int(rule.risk_score)

                    elif rule.parameter == RuleParameterEnum.DATA_MATCH_LESS_THAN:

                        if int(rule_comparison_value) < int(rule.value):

                            total_risk_score += int(rule.risk_score)

                    elif rule.parameter == RuleParameterEnum.DATA_COMPARISON_EXISTS_IN:

                        if rule_comparison_value in rule.value:

                            total_risk_score += int(rule.risk_score)

                    elif (
                        rule.parameter
                        == RuleParameterEnum.DATA_COMPARISON_EXISTS_NOT_IN
                    ):

                        if rule_comparison_value not in rule.value:

                            total_risk_score += int(rule.risk_score)

                    else:

                        continue

            if int(total_risk_score / total_rules_count) > 70:

                session.body = {
                    "message": "This transaction has been flagged for fruad by our system, please contact card issuer"
                }

                response = Response(
                    json.dumps(session.body),
                    media_type="application/json",
                    status_code=403,
                )

                api_helper.post(
                    url=f"{constants.BWATCH_DECISION_SERVICE_BASE_URL}/v1/fraudulent_customers/{bwatch_python_data_context.app_id}/{id_to_track_on_middleware}",
                    data={},
                )

                return response

    return None


def process_as_middleware(url: str, body: dict):

    session = SessionProperties(
        method="",
        url=url,
        headers="",
        query_params="",
        path_params="",
        client="",
        cookies="",
        body=dict(body),
    )

    fraudulent_customers_dict = bwatch_python_data_context.fraudulent_customers_dict

    id_to_track_on_middleware = bwatch_python_data_context.id_to_track_on_middleware

    id_to_track_on_middleware = session.body.get(id_to_track_on_middleware)

    if id_to_track_on_middleware in fraudulent_customers_dict and fraudulent_customers_dict.get(id_to_track_on_middleware):

        session.body = {
            "message": "This user has been flagged for fruad by our system, please contact card issuer"
        }

        response = Response(
            json.dumps(session.body), media_type="application/json", status_code=403
        )

        return response

    else:

        session_copy = copy.deepcopy(session.body)

        transactions_data_mappers_copy = copy.deepcopy(
            bwatch_python_data_context.transactions_data_mappers
        )

        create_transaction(
            session_copy,
            mapping=transactions_data_mappers_copy,
        )

        result = fetch_usecase_rules(
            rules=bwatch_python_data_context.high_urgency_usecase_rules_dict
        )

        usecase_rules = result.get("data")

        transaction_data_dict = data_mapper(
            data=session_copy,
            mapping=transactions_data_mappers_copy,
        )

        if usecase_rules:

            total_rules_count = len(usecase_rules)

            total_risk_score = 0

            for rule in usecase_rules:

                rule = Rule(**rule)

                rule_key_list = rule.key.split(".")

                rule_comparison_value = 0

                if rule_key_list[0] == "transactions":

                    for key_index in range(len(rule_key_list)):

                        if key_index == 0:

                            continue

                        elif key_index == 1:

                            rule_comparison_value = transaction_data_dict.get(
                                rule_key_list[key_index].lstrip().rstrip()
                            )

                        else:

                            rule_comparison_value = rule_comparison_value.get(
                                rule_key_list[key_index].lstrip().rstrip()
                            )

                    if rule.parameter == RuleParameterEnum.DATA_COMPARISON_EQUAL_TO:

                        if rule_comparison_value == rule.value:

                            total_risk_score += int(rule.risk_score)

                    elif (
                        rule.parameter == RuleParameterEnum.DATA_COMPARISON_NOT_EQUAL_TO
                    ):

                        if rule_comparison_value != rule.value:

                            total_risk_score += int(rule.risk_score)

                    elif rule.parameter == RuleParameterEnum.DATA_MATCH_GREATER_THAN:

                        if int(float(rule_comparison_value)) > int(float(rule.value)):

                            print(rule_comparison_value, rule.value)

                            total_risk_score += int(rule.risk_score)

                    elif rule.parameter == RuleParameterEnum.DATA_MATCH_LESS_THAN:

                        if int(rule_comparison_value) < int(rule.value):

                            total_risk_score += int(rule.risk_score)

                    elif rule.parameter == RuleParameterEnum.DATA_COMPARISON_EXISTS_IN:

                        if rule_comparison_value in rule.value:

                            total_risk_score += int(rule.risk_score)

                    elif (
                        rule.parameter
                        == RuleParameterEnum.DATA_COMPARISON_EXISTS_NOT_IN
                    ):

                        if rule_comparison_value not in rule.value:

                            total_risk_score += int(rule.risk_score)

                    else:

                        continue

            if int(total_risk_score / total_rules_count) > 70:

                session.body = {
                    "message": "This transaction has been flagged for fruad by our system, please contact card issuer"
                }

                response = Response(
                    json.dumps(session.body),
                    media_type="application/json",
                    status_code=403,
                )

                api_helper.post(
                    url=f"{constants.BWATCH_DECISION_SERVICE_BASE_URL}/v1/fraudulent_customers/{bwatch_python_data_context.app_id}/{id_to_track_on_middleware}",
                    data={},
                )
                return response

    return None
