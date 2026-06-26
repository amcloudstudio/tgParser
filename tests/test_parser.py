from unittest.mock import MagicMock

from telethon.errors import ChannelPrivateError

from src.parser.telegram_parser import TelegramParser


def _make_parser_with_client(client):
    parser = TelegramParser.__new__(TelegramParser)
    parser.client = client
    return parser


def test_fetch_messages_handles_access_error():
    client = MagicMock()
    client.iter_messages.side_effect = ChannelPrivateError(request=None)
    parser = _make_parser_with_client(client)

    result = parser.fetch_messages("@private_chan")

    assert result == []


def test_fetch_messages_skips_empty_text_messages():
    msg = MagicMock()
    msg.text = None
    client = MagicMock()
    client.iter_messages.return_value = [msg]
    parser = _make_parser_with_client(client)

    result = parser.fetch_messages("@chan1")

    assert result == []
