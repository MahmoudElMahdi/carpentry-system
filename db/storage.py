import json
import os
from typing import Any, List, Dict

class Storage:
    def __init__(self, db_path: str = "data"):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

    def _get_file_path(self, collection: str) -> str:
        return os.path.join(self.db_path, f"{collection}.json")

    def load(self, collection: str) -> List[Dict[str, Any]]:
        file_path = self._get_file_path(collection)
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save(self, collection: str, data: List[Dict[str, Any]]):
        file_path = self._get_file_path(collection)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def append(self, collection: str, item: Dict[str, Any]):
        data = self.load(collection)
        data.append(item)
        self.save(collection, data)
