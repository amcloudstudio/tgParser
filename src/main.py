from .config.settings import ConfigError, load_settings
from .parser.telegram_parser import TelegramParser
from .storage.json_storage import get_storage
from .utils.logger import get_logger

logger = get_logger(__name__)


def run():
    try:
        settings = load_settings()
    except ConfigError as exc:
        logger.error("Configuration error: %s", exc)
        return

    if not settings.targets:
        logger.warning("No TARGETS configured in .env, nothing to do.")
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


if __name__ == "__main__":
    run()
