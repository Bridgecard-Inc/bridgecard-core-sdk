import os
from typing import Optional
import slack_sdk


class SlackClient:
    def __init__(self) -> None:
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN_CHANNEL_WRITE")

        self._client = slack_sdk.WebClient(token=slack_bot_token)

    def send_message(
        self, message: str, channel_id: str, thread_ts: Optional[str] = None
    ):
        res = self._client.chat_postMessage(
            channel=channel_id,
            text=message,
            thread_ts=thread_ts,
        )

        ts = res.get("ts")

        return ts
