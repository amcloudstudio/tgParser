import csv
import json

from src.storage.csv_storage import CSVStorage
from src.storage.json_storage import JSONStorage, get_storage

SAMPLE_MESSAGES = [
    {
        "message_id": 1,
        "date": "2024-01-01T00:00:00",
        "chat": "@chan1",
        "sender_id": 42,
        "sender_name": "alice",
        "text": "hello",
    }
]


def test_csv_storage_writes_rows(tmp_path):
    storage = CSVStorage(str(tmp_path))
    path = storage.save("@chan1", SAMPLE_MESSAGES)

    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 1
    assert rows[0]["text"] == "hello"


def test_json_storage_writes_list(tmp_path):
    storage = JSONStorage(str(tmp_path))
    path = storage.save("@chan1", SAMPLE_MESSAGES)

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    assert data == SAMPLE_MESSAGES


def test_csv_storage_handles_empty_result(tmp_path):
    storage = CSVStorage(str(tmp_path))
    path = storage.save("@empty", [])

    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows == []


def test_get_storage_selects_backend(tmp_path):
    assert isinstance(get_storage("json", str(tmp_path)), JSONStorage)
    assert isinstance(get_storage("csv", str(tmp_path)), CSVStorage)
