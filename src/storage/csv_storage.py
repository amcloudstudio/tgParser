import csv
import os

from .base import Storage

FIELDNAMES = ["message_id", "date", "chat", "sender_id", "sender_name", "text"]


class CSVStorage(Storage):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def save(self, target: str, messages) -> str:
        os.makedirs(self.output_dir, exist_ok=True)
        safe_name = target.lstrip("@").replace("/", "_")
        path = os.path.join(self.output_dir, f"{safe_name}.csv")

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for message in messages:
                writer.writerow({key: message.get(key, "") for key in FIELDNAMES})

        return path
