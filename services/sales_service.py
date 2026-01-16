from db.storage import Storage
from models.project import Project
from models.transaction import Transaction
from typing import List, Dict

class SalesService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def create_project(self, name: str, customer_id: str, total_value: float, description: str = "") -> Project:
        project = Project(
            name=name, 
            customer_id=customer_id, 
            total_value=total_value, 
            description=description
        )
        self.storage.append('projects', project.to_dict())
        return project

    def list_projects(self, status: str = None) -> List[Project]:
        all_projects = [Project.from_dict(p) for p in self.storage.load('projects')]
        if status:
            return [p for p in all_projects if p.status == status]
        return all_projects

    def get_project_summary(self, project_id: str) -> Dict:
        """Calculates paid amount and remaining balance for a project."""
        projects = self.list_projects()
        project = next((p for p in projects if p.id == project_id), None)
        if not project:
            return {}

        transactions = [Transaction.from_dict(t) for t in self.storage.load('transactions')]
        
        # Filter transactions related to this project (using related_id for now)
        # Note: We need to ensure when recording sale we use related_id=project_id
        project_transactions = [t for t in transactions if t.related_id == project_id and t.type == 'SALE']
        
        paid_amount = sum(t.amount for t in project_transactions)
        remaining = project.total_value - paid_amount
        
        return {
            "project": project,
            "paid": paid_amount,
            "remaining": remaining,
            "transactions": project_transactions
        }

    def get_tax_report(self) -> Dict:
        """Calculates VAT In (Collected) vs VAT Out (Paid)."""
        transactions = [Transaction.from_dict(t) for t in self.storage.load('transactions')]
        
        vat_collected = 0.0 # From Sales
        vat_paid = 0.0      # From Purchases/Expenses
        
        for t in transactions:
            if t.type == 'SALE':
                vat_collected += t.tax_amount
            elif t.type in ['PURCHASE', 'EXPENSE']:
                vat_paid += t.tax_amount
                
        return {
            "vat_collected": vat_collected,
            "vat_paid": vat_paid,
            "net_vat": vat_collected - vat_paid
        }
