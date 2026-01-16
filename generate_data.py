
import json
import random
from datetime import datetime, timedelta
import uuid

# Configuration
DATA_FILE = "db/data.json"
NUM_TRANSACTIONS = 50
START_DATE = datetime.now() - timedelta(days=90)

# Categories
EXPENSE_CATEGORIES = ["Raw Materials", "Rent", "Utilities", "Transportation", "Tools", "Marketing"]
INCOME_CATEGORIES = ["Project Payment", "Consultation", "Repair Service"]
PAYMENT_METHODS = ["Cash", "Bank Transfer", "Credit Card"]
PAYMENT_SOURCES = ["Company Account", "Petty Cash"]

def generate_data():
    data = {
        "transactions": [],
        "projects": [],
        "products": [],
        "materials": [],
        "contacts": []
    }

    # Generate Transactions
    current_date = START_DATE
    while current_date <= datetime.now():
        # 70% chance of transaction on any given day
        if random.random() < 0.7:
            is_income = random.random() < 0.4 # 40% income, 60% expense
            
            t_type = "SALE" if is_income else "EXPENSE"
            cat = random.choice(INCOME_CATEGORIES) if is_income else random.choice(EXPENSE_CATEGORIES)
            
            amount = random.randint(500, 5000) if is_income else random.randint(50, 800)
            
            transaction = {
                "id": str(uuid.uuid4()),
                "date": current_date.strftime("%Y-%m-%d"),
                "type": t_type,
                "category": cat,
                "description": f"{cat} - {random.choice(['Batch A', ' Urgent', 'Restock', 'Service'])}",
                "amount": float(amount),
                "payment_method": random.choice(PAYMENT_METHODS),
                "payment_source": random.choice(PAYMENT_SOURCES),
                "is_paid": True,
                "tax_amount": float(amount * 0.1) if random.random() > 0.5 else 0.0,
                "contact_id": None,
                "related_id": None
            }
            data["transactions"].append(transaction)
        
        current_date += timedelta(days=1)

    # Save to file
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Generated {len(data['transactions'])} transactions.")

if __name__ == "__main__":
    generate_data()
