from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import Channel, Chat

from ..utils.logger import get_logger

logger = get_logger(__name__)


def search_channels(client, keywords, limit: int = 20):
    """Search public channels/chats by keyword via Telegram's own search index.

    Uses the same global search exposed in the Telegram app UI. Does not join,
    message, or scrape members of any found chat - only public title/username.
    Returns a deduplicated list of dicts.
    """
    results = {}

    for keyword in keywords:
        try:
            response = client(SearchRequest(q=keyword, limit=limit))
        except Exception:
            logger.exception("Keyword search failed for '%s'", keyword)
            continue

        for chat in response.chats:
            if not isinstance(chat, (Channel, Chat)):
                continue
            results[chat.id] = {
                "id": chat.id,
                "title": chat.title,
                "username": getattr(chat, "username", "") or "",
                "type": "channel" if isinstance(chat, Channel) else "chat",
                "keyword": keyword,
            }

    return list(results.values())
