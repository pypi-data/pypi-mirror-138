"""Functions that assist in building and sending text messages.
"""
import os
from logging import WARNING, getLogger

from twilio.rest import Client

logger = getLogger()
logger.setLevel(WARNING)


class TextMessage:
    def __init__(self) -> None:
        self._check_if_credentials_set()
        self.message_lines = []

    def __repr__(self) -> str:
        return f"TextMessage(\n\t{self.message}\n)"

    def __str__(self) -> str:
        return self.__repr__()

    def __length__(self) -> int:
        return len(self.message)

    @classmethod
    def _check_if_credentials_set(cls, action="warning") -> bool:
        warning_or_error_message = (
            "To send messages please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN."
        )
        if cls._are_credentials_set() is False:
            if action == "warning":
                logger.warning(warning_or_error_message)
                return False
            elif action == "raise":
                raise Exception(warning_or_error_message)
            else:
                raise Exception(f"Invalid action {action}.")

    @staticmethod
    def _are_credentials_set() -> bool:
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        return account_sid is not None and auth_token is not None

    @property
    def message(self) -> str:
        return "\n\t".join(self.message_lines)

    def add_line(self, text: str) -> "TextMessage":
        """Adds a line of text to the text message.

        Args:
            text (str): Line of text to be added to the message.
        """
        self.message_lines.append(text)
        return self

    def reset_message(self) -> "TextMessage":
        """Resets the contents of the text message."""
        self.message_lines = []
        return self

    def send(self, to: str, from_: str):
        """Sends the text message to the specified number.

        Args:
            to (str): Number to send message to.
            from_ (str): Number the message is sent from. Should be your active Twilio number.
        """
        self._check_if_credentials_set(action="raise")
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        return client.messages.create(to, body=self.message, from_=from_)