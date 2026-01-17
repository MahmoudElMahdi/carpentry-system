import json
import os
from typing import Any, List, Dict

class Storage:
    def __init__(self, db_path: str = "db/data.json"):
        self.db_file = db_path
        self._cache = None
        self._load_all_data()

    def _load_all_data(self):
        """Load all data from the consolidated JSON file"""
        if not os.path.exists(self.db_file):
            self._cache = {}
            return
        try:
            with open(self.db_file, 'r') as f:
                self._cache = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._cache = {}

    def _save_all_data(self):
        """Save all data back to the consolidated JSON file"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        with open(self.db_file, 'w') as f:
            json.dump(self._cache, f, indent=4)

    def load(self, collection: str) -> List[Dict[str, Any]]:
        """Load a specific collection from the data"""
        return self._cache.get(collection, [])

    def save(self, collection: str, data: List[Dict[str, Any]]):
        """Save data to a specific collection"""
        self._cache[collection] = data
        self._save_all_data()

    def append(self, collection: str, item: Dict[str, Any]):
        """Append an item to a collection"""
        if collection not in self._cache:
            self._cache[collection] = []
        self._cache[collection].append(item)
        self._save_all_data()
