import os

from .config.settings import ConfigError, load_settings
from .parser.channel_search import search_channels
from .parser.telegram_parser import TelegramParser
from .storage.generic import save_csv, save_json
from .storage.json_storage import get_storage
from .utils.logger import get_logger

logger = get_logger(__name__)


def run():
    try:
        settings = load_settings()
    except ConfigError as exc:
        logger.error("Configuration error: %s", exc)
        return

    if not settings.targets and not settings.target_keywords:
        logger.warning("No TARGETS or TARGET_KEYWORDS configured in .env, nothing to do.")
        return

    storage = get_storage(settings.output_format, settings.output_dir)

    with TelegramParser(
        settings.api_id, settings.api_hash, settings.session_name
    ) as parser:
        for target in settings.targets:
            logger.info("Fetching messages from '%s'", target)
            messages = parser.fetch_messages(target)
            if not messages:
                logger.info("No messages collected for '%s'", target)
                continue
            path = storage.save(target, messages)
            logger.info("Saved %d messages from '%s' to %s", len(messages), target, path)

        if settings.target_keywords:
            logger.info("Searching public channels/chats for keywords: %s", settings.target_keywords)
            found = search_channels(parser.client, settings.target_keywords)
            if not found:
                logger.info("No channels/chats found for given keywords.")
            else:
                ext = "json" if settings.output_format == "json" else "csv"
                path = os.path.join(settings.output_dir, f"channel_search.{ext}")
                if settings.output_format == "json":
                    save_json(path, found)
                else:
                    save_csv(path, found)
                logger.info("Saved %d found channels/chats to %s", len(found), path)


if __name__ == "__main__":
    run()
