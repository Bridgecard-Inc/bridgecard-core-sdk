from datetime import datetime
import ssl
from ..slack.slack_client import SlackClient

ssl._create_default_https_context = ssl._create_unverified_context


slack_client = SlackClient()


class BackgoundTaskMonitor:
    def __init__(self, task_name) -> None:
        self._task_name = task_name
        self._monitor_channel_id = "C06021NVCKD"
        self._call_counter = 0

        current_time = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}-{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}"

        self._monitor_message_ts = slack_client.send_message(
            message=f"{self._task_name} STARTED AT {current_time}",
            channel_id=self._monitor_channel_id,
        )

    def dispatch_alive_event(self, event) -> None:

        # This helps us only dispatch events to slack after every 20 event dispatch from the function

        self._call_counter+=1

        if self._call_counter % 40 == 0:

            slack_client.send_message(
                message=event,
                channel_id=self._monitor_channel_id,
                thread_ts=self._monitor_message_ts
            )

    def dispatch_error_event(self, event) -> None:

        slack_client.send_message(
            message=f"ERROR {event} on {self._task_name}",
            channel_id=self._monitor_channel_id,
            thread_ts=self._monitor_message_ts
        )
