import csv
import json
import os

DEFAULT_FIELDNAMES = ["id", "title", "username", "type", "keyword"]


def save_csv(path: str, records) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = list(records[0].keys()) if records else DEFAULT_FIELDNAMES

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def save_json(path: str, records) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
