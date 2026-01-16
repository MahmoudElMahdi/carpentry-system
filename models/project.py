from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Project:
    name: str
    customer_id: str
    total_value: float  # Agreed contract amount
    start_date: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "Active"  # 'Active', 'Completed', 'Cancelled'
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Project(**data)
