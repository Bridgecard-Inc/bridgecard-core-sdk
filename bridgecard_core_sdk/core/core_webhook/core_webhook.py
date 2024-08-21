from contextlib import AbstractContextManager, contextmanager
import json
import time
from redis import Redis
import os
from typing import Any, Callable, Optional
from fastapi import Header

from starlette.requests import Request

from bridgecard_core_sdk.core.core_db.schema.base_schema import EnvironmentEnum
from bridgecard_core_sdk.core.core_webhook.schema.base_schema import WebhookEventSession
from bridgecard_core_sdk.core.core_webhook.utils.core_webhook_data_context import (
    core_webhook_data_context,
)
from bridgecard_core_sdk.core.utils.rabbitmq.publisher import BasicMessageSender


def init_core_webhook():
    rabbitmq_broker_id = os.environ.get("RABBIT_MQ_BROKER_ID")

    rabbitmq_user = os.environ.get("RABBIT_MQ_USER")

    rabbitmq_password = os.environ.get("RABBIT_MQ_PASSWORD")

    region = os.environ.get("REGION")

    basic_message_sender = BasicMessageSender(
        rabbitmq_broker_id,
        rabbitmq_user,
        rabbitmq_password,
        region,
    )

    core_webhook_data_context.basic_message_sender = basic_message_sender


def process_webhook(queue_name: str, webhook_event_session: WebhookEventSession):
    
    init_core_webhook()
    
    core_webhook_data_context.basic_message_sender.declare_queue(queue_name)

    data_to_send = webhook_event_session.dict()

    json_body = json.dumps(data_to_send)

    # Send a message to the queue.
    core_webhook_data_context.basic_message_sender.send_message(
        exchange="", routing_key=queue_name, body=json_body
    )

    core_webhook_data_context.basic_message_sender.close()
