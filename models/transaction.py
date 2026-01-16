from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid

@dataclass
class Transaction:
    type: str  # 'PURCHASE', 'SALE', 'EXPENSE', 'PAYROLL'
    amount: float
    description: str
    category: str = "General"  # e.g., 'Raw Materials', 'Rent', 'Salary'
    payment_method: str = "Cash"  # 'Cash', 'Bank Transfer', 'Cheque'
    payment_source: str = "Company"  # 'Company', 'Personal'
    tax_amount: float = 0.0
    contact_id: Optional[str] = None  # Link to Supplier/Employee/Customer
    is_paid: bool = True
    date: str = field(default_factory=lambda: datetime.now().isoformat())
    related_id: Optional[str] = None  # ID of material/product
    quantity: float = 0.0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Transaction(**data)
