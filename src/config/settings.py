import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


class ConfigError(Exception):
    pass


@dataclass
class Settings:
    api_id: int
    api_hash: str
    session_name: str
    targets: list = field(default_factory=list)
    target_keywords: list = field(default_factory=list)
    output_format: str = "csv"
    output_dir: str = "data/output"


def load_settings(env_path: str = ".env") -> Settings:
    load_dotenv(env_path)

    api_id_raw = os.getenv("API_ID", "").strip()
    api_hash = os.getenv("API_HASH", "").strip()
    session_name = os.getenv("SESSION_NAME", "telegram_parser").strip()
    targets_raw = os.getenv("TARGETS", "").strip()
    keywords_raw = os.getenv("TARGET_KEYWORDS", "").strip()
    output_format = os.getenv("OUTPUT_FORMAT", "csv").strip().lower()
    output_dir = os.getenv("OUTPUT_DIR", "data/output").strip()

    if not api_id_raw or not api_hash:
        raise ConfigError("API_ID and API_HASH must be set in .env")

    try:
        api_id = int(api_id_raw)
    except ValueError as exc:
        raise ConfigError("API_ID must be an integer") from exc

    if output_format not in ("csv", "json"):
        raise ConfigError("OUTPUT_FORMAT must be 'csv' or 'json'")

    targets = [t.strip() for t in targets_raw.split(",") if t.strip()]
    target_keywords = [k.strip() for k in keywords_raw.split("|") if k.strip()]

    return Settings(
        api_id=api_id,
        api_hash=api_hash,
        session_name=session_name,
        targets=targets,
        target_keywords=target_keywords,
        output_format=output_format,
        output_dir=output_dir,
    )
