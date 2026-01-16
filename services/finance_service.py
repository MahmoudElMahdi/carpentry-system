from db.storage import Storage
from models.transaction import Transaction
from models.contact import Contact
from typing import List, Optional, Dict

class FinanceService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def add_contact(self, name: str, role: str, phone: str = "") -> Contact:
        contact = Contact(name=name, role=role, phone=phone)
        self.storage.append('contacts', contact.to_dict())
        return contact

    def list_contacts(self, role: Optional[str] = None) -> List[Contact]:
        all_contacts = [Contact.from_dict(c) for c in self.storage.load('contacts')]
        if role:
            return [c for c in all_contacts if c.role == role]
        return all_contacts

    def record_transaction(self, 
                           type: str, 
                           amount: float, 
                           description: str, 
                           category: str = "General",
                           payment_method: str = "Cash",
                           payment_source: str = "Company",
                           tax_amount: float = 0.0,
                           contact_id: Optional[str] = None,
                           related_id: str = None, 
                           quantity: float = 0.0,
                           date: str = None) -> Transaction:
        
        transaction = Transaction(
            type=type,
            amount=amount,
            description=description,
            category=category,
            payment_method=payment_method,
            payment_source=payment_source,
            tax_amount=tax_amount,
            contact_id=contact_id,
            related_id=related_id,
            quantity=quantity
        )
        if date:
            transaction.date = date
        self.storage.append('transactions', transaction.to_dict())
        
        # Update Contact Balance if applicable (Logic to be refined)
        # For now, just logging
        print(f"Transaction recorded: {type} - {amount} ({payment_source})")
        return transaction

    def get_balance(self) -> float:
        transactions = [Transaction.from_dict(t) for t in self.storage.load('transactions')]
        balance = 0.0
        for t in transactions:
            if t.payment_source == 'Company':
                if t.type == 'SALE':
                    balance += t.amount
                elif t.type in ['PURCHASE', 'EXPENSE', 'PAYROLL']:
                    balance -= t.amount
        return balance

    def get_financial_summary(self) -> Dict:
        transactions = [Transaction.from_dict(t) for t in self.storage.load('transactions')]
        
        total_revenue = sum(t.amount for t in transactions if t.type == 'SALE')
        total_expenses = sum(t.amount for t in transactions if t.type in ['PURCHASE', 'EXPENSE', 'PAYROLL'])
        
        # Calculate Cash on Hand (Company Source)
        cash_on_hand = 0.0
        for t in transactions:
            if t.payment_source == 'Company':
                 if t.type == 'SALE': cash_on_hand += t.amount
                 elif t.type in ['PURCHASE', 'EXPENSE', 'PAYROLL']: cash_on_hand -= t.amount

        return {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_profit": total_revenue - total_expenses,
            "cash_on_hand": cash_on_hand
        }

    def get_monthly_trends(self) -> Dict:
        transactions = [Transaction.from_dict(t) for t in self.storage.load('transactions')]
        trends = {} # Format: "YYYY-MM": {"income": 0, "expense": 0}
        
        for t in transactions:
            month_key = t.date[:7] # YYYY-MM
            if month_key not in trends:
                trends[month_key] = {"income": 0.0, "expense": 0.0}
            
            if t.type == 'SALE':
                trends[month_key]["income"] += t.amount
            elif t.type in ['PURCHASE', 'EXPENSE', 'PAYROLL']:
                trends[month_key]["expense"] += t.amount
        
        # Sort by month
        sorted_keys = sorted(trends.keys())
        return {
            "labels": sorted_keys,
            "income": [trends[k]["income"] for k in sorted_keys],
            "expense": [trends[k]["expense"] for k in sorted_keys]
        }
    
    def get_expense_breakdown(self) -> Dict:
        transactions = [Transaction.from_dict(t) for t in self.storage.load('transactions')]
        breakdown = {"Raw Materials": 0.0, "Payroll": 0.0, "Rent": 0.0, "Other": 0.0}
        
        for t in transactions:
            if t.type in ['PURCHASE', 'EXPENSE', 'PAYROLL']:
                # Simple mapping based on type/category
                if t.type == 'PAYROLL':
                    breakdown["Payroll"] += t.amount
                elif t.category in list(breakdown.keys()):
                    breakdown[t.category] += t.amount
                elif "Material" in t.category:
                    breakdown["Raw Materials"] += t.amount
                else:
                    breakdown["Other"] += t.amount
        
        return breakdown
