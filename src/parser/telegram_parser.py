from telethon.errors import (
    ChannelPrivateError,
    ChatAdminRequiredError,
    UsernameNotOccupiedError,
)
from telethon.sync import TelegramClient

from ..utils.logger import get_logger

logger = get_logger(__name__)


class TelegramParser:
    """Reads message history from chats/channels the account already has access to.

    Does not attempt to join chats, bypass privacy settings, or send messages.
    """

    def __init__(self, api_id: int, api_hash: str, session_name: str):
        self.client = TelegramClient(session_name, api_id, api_hash)

    def __enter__(self):
        self.client.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.disconnect()

    def fetch_messages(self, target: str, limit: int = 100):
        """Fetch up to `limit` recent messages from a single chat/channel.

        Returns an empty list if the chat is inaccessible or has no messages.
        """
        messages = []
        try:
            for message in self.client.iter_messages(target, limit=limit):
                if not message.text:
                    continue
                sender = message.sender
                sender_name = getattr(sender, "username", None) or getattr(
                    sender, "first_name", ""
                )
                messages.append(
                    {
                        "message_id": message.id,
                        "date": message.date.isoformat() if message.date else "",
                        "chat": target,
                        "sender_id": getattr(sender, "id", ""),
                        "sender_name": sender_name or "",
                        "text": message.text,
                    }
                )
        except (ChannelPrivateError, ChatAdminRequiredError):
            logger.warning("No access to '%s', skipping.", target)
        except UsernameNotOccupiedError:
            logger.warning("Target '%s' does not exist, skipping.", target)
        except Exception:
            logger.exception("Failed to fetch messages from '%s'.", target)

        return messages
