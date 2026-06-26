import os

import pytest

from src.config.settings import ConfigError, load_settings


def test_load_settings_success(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "API_ID=12345\nAPI_HASH=abc\nSESSION_NAME=test_session\n"
        "TARGETS=@chan1, @chan2\nOUTPUT_FORMAT=json\nOUTPUT_DIR=out\n"
    )
    for key in ("API_ID", "API_HASH", "SESSION_NAME", "TARGETS", "OUTPUT_FORMAT", "OUTPUT_DIR"):
        monkeypatch.delenv(key, raising=False)

    settings = load_settings(str(env_file))

    assert settings.api_id == 12345
    assert settings.api_hash == "abc"
    assert settings.targets == ["@chan1", "@chan2"]
    assert settings.output_format == "json"


def test_load_settings_missing_credentials(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("SESSION_NAME=test_session\n")
    for key in ("API_ID", "API_HASH"):
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(ConfigError):
        load_settings(str(env_file))


def test_load_settings_invalid_output_format(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("API_ID=1\nAPI_HASH=abc\nOUTPUT_FORMAT=xml\n")
    for key in ("API_ID", "API_HASH", "OUTPUT_FORMAT"):
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(ConfigError):
        load_settings(str(env_file))
