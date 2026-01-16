from dataclasses import dataclass, field
import uuid
from typing import Optional

@dataclass
class Contact:
    name: str
    role: str  # 'SUPPLIER', 'CUSTOMER', 'EMPLOYEE'
    phone: str = ""
    email: str = ""
    address: str = ""
    current_balance: float = 0.0  # + means they owe us, - means we owe them
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Contact(**data)
