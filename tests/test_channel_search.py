from unittest.mock import MagicMock

from telethon.tl.types import Channel

from src.parser.channel_search import search_channels


def _make_channel(chat_id, title, username):
    channel = MagicMock(spec=Channel)
    channel.id = chat_id
    channel.title = title
    channel.username = username
    return channel


def test_search_channels_deduplicates_results():
    channel = _make_channel(1, "Test Channel", "testchannel")
    client = MagicMock()
    client.return_value.chats = [channel]

    found = search_channels(client, ["keyword1", "keyword2"])

    assert len(found) == 1
    assert found[0]["id"] == 1
    assert found[0]["username"] == "testchannel"


def test_search_channels_handles_empty_result():
    client = MagicMock()
    client.return_value.chats = []

    found = search_channels(client, ["no_such_keyword"])

    assert found == []


def test_search_channels_handles_request_error():
    client = MagicMock()
    client.side_effect = Exception("network error")

    found = search_channels(client, ["keyword"])

    assert found == []
