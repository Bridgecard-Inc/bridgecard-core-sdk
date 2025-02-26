import os
from typing import IO, Optional, Union
import slack_sdk


class SlackClient:
    def __init__(self) -> None:
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN_CHANNEL_WRITE")

        self._client = slack_sdk.WebClient(token=slack_bot_token)

    def send_message(
        self,
        message: str,
        channel_id: str,
        thread_ts: Optional[str] = None,
        blocks: Optional[str] = None,
    ):
        res = self._client.chat_postMessage(
            channel=channel_id,
            text=message,
            thread_ts=thread_ts,
            blocks=blocks
        )

        ts = res.get("ts")

        return ts

    def upload_file(
        self,
        channels: Union[str, list],
        file: Union[str, IO],
        filename: Optional[str] = None,
        initial_comment: Optional[str] = None,
        thread_ts: Optional[str] = None,
    ):
        """
        Upload a file to Slack.
        :param channels: Channel ID(s) to share the file to (string or list of strings)
        :param file: File content or path to the file
        :param filename: Filename of the file (optional)
        :param initial_comment: Initial comment to add to the file (optional)
        :param thread_ts: Thread timestamp to upload the file to (optional)
        :return: Response from Slack API
        """
        if isinstance(channels, list):
            channels = ",".join(channels)
        # Ensure file is opened if it's a path
        if isinstance(file, str):
            with open(file, 'rb') as f:
                res = self._client.files_upload_v2(
                    channels=channels,
                    file=f,
                    filename=filename,
                    initial_comment=initial_comment,
                    thread_ts=thread_ts
                )
        else:
            res = self._client.files_upload_v2(
                channels=channels,
                file=file,
                filename=filename,
                initial_comment=initial_comment,
                thread_ts=thread_ts
            )
        return res
    
    def delete_message(self, channel: str, ts: str):
       """
       Delete a message from Slack.
       :param channel: Channel ID where the message is located
       :param ts: Timestamp of the message to delete
       :return: Response from Slack API
       """
       try:
           response = self._client.chat_delete(channel=channel, ts=ts)
           return response
       except slack_sdk.errors.SlackApiError as e:
           print(f"Error deleting message: {e.response['error']}")
           return None

    # In your SlackClient class
    def delete_file(self, file_id: str):
        """
        Delete a file from Slack.
        :param file_id: ID of the file to delete
        :return: Response from Slack API
        """
        
        try:
            self._client.files_delete(file=file_id)
            print(f"File {file_id} deleted successfully")
        except Exception as e:
            print(f"Failed to delete Slack file {file_id}: {str(e)}")