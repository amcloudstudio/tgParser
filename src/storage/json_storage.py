import json
import os

from .base import Storage


class JSONStorage(Storage):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def save(self, target: str, messages) -> str:
        os.makedirs(self.output_dir, exist_ok=True)
        safe_name = target.lstrip("@").replace("/", "_")
        path = os.path.join(self.output_dir, f"{safe_name}.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(list(messages), f, ensure_ascii=False, indent=2)

        return path


def get_storage(output_format: str, output_dir: str):
    if output_format == "json":
        return JSONStorage(output_dir)
    from .csv_storage import CSVStorage

    return CSVStorage(output_dir)
