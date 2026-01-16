from dataclasses import dataclass, field
import uuid

@dataclass
class Material:
    name: str
    unit: str  # e.g., 'm3', 'pcs'
    cost_per_unit: float
    stock_quantity: float = 0.0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Material(**data)
