from db.storage import Storage
from services.inventory_service import InventoryService
from services.finance_service import FinanceService
from services.sales_service import SalesService
from datetime import datetime, timedelta
import random

# Initialize Services
storage = Storage()
inventory = InventoryService(storage)
finance = FinanceService(storage)
sales = SalesService(storage)

print("Clearing old data...")
# Optional: Clear existing data files if you want a fresh start
# import os
# for f in ['data/contacts.json', 'data/transactions.json', 'data/projects.json', 'data/materials.json']:
#     if os.path.exists(f): os.remove(f)

print("Populating Contacts...")
# Suppliers
wood_supp = finance.add_contact("El-Nour Woods", "SUPPLIER", "01012345678")
paint_supp = finance.add_contact("Modern Paints Co.", "SUPPLIER", "01123456789")
tool_supp = finance.add_contact("Hardware Pro", "SUPPLIER", "01234567890")

# Employees
worker1 = finance.add_contact("Ahmed Hassan", "EMPLOYEE", "0100000001")
worker2 = finance.add_contact("Mohamed Ali", "EMPLOYEE", "0100000002")

# Customers
client1 = finance.add_contact("Dr. Tarek", "CUSTOMER", "0122222222")
client2 = finance.add_contact("Eng. Sarah", "CUSTOMER", "0155555555")

print("Populating Inventory...")
inventory.add_material("Swedish Wood 2x4", "m3", 12000.0)
inventory.add_material("Plywood 18mm", "sheet", 850.0)
inventory.add_material("White Paint", "kg", 150.0)
inventory.add_material("Screws 5cm", "box", 200.0)

print("Creating Projects...")
proj1 = sales.create_project("Villa Tarek Kitchen", client1.id, 75000.0, "Luxury kitchen with island")
proj2 = sales.create_project("Sarah Apartment Doors", client2.id, 45000.0, "10 interior doors")

print("Recording Transactions (Backdated)...")
# Helper to get date string
def days_ago(n):
    return (datetime.now() - timedelta(days=n)).isoformat()

# 1. Initial Investment / Purchase
finance.record_transaction(
    type="PURCHASE", 
    amount=24000.0, 
    description="2m3 Swedish Wood", 
    category="Raw Materials", 
    payment_source="Company",
    contact_id=wood_supp.id,
    date=days_ago(30)
)
finance.record_transaction(
    type="PURCHASE", 
    amount=5000.0, 
    description="Paint and thinner", 
    category="Raw Materials", 
    payment_source="Company",
    contact_id=paint_supp.id,
    date=days_ago(28)
)

# 2. Project 1: Advance Payment
finance.record_transaction(
    type="SALE", 
    amount=30000.0, 
    description="Down Payment - Villa Tarek", 
    category="Project Payment", 
    payment_source="Company", 
    contact_id=client1.id,
    related_id=proj1.id,
    tax_amount=3000.0, # VAT
    date=days_ago(25)
)

# 3. Expenses
finance.record_transaction(
    type="EXPENSE", 
    amount=3500.0, 
    description="Workshop Rent - Jan", 
    category="Rent", 
    payment_source="Company",
    date=days_ago(20)
)

# 4. Payroll
finance.record_transaction(
    type="PAYROLL", 
    amount=500.0, 
    description="Ahmed Advance", 
    category="Advance", 
    payment_source="Company", 
    contact_id=worker1.id,
    date=days_ago(15)
)

# 5. Purchases from Personal Pocket (Owner Funding)
finance.record_transaction(
    type="PURCHASE", 
    amount=1200.0, 
    description="Emergency Nails/Glue", 
    category="Tools", 
    payment_source="Personal",
    contact_id=tool_supp.id,
    date=days_ago(10)
)

# 6. Project 1: Second Payment
finance.record_transaction(
    type="SALE", 
    amount=20000.0, 
    description="2nd Installment - Villa Tarek", 
    category="Project Payment", 
    payment_source="Company", 
    contact_id=client1.id,
    related_id=proj1.id,
    tax_amount=2000.0,
    date=days_ago(5)
)

# 7. Project 2: Start
finance.record_transaction(
    type="SALE", 
    amount=15000.0, 
    description="Down Payment - Interior Doors", 
    category="Project Payment", 
    payment_source="Company", 
    contact_id=client2.id,
    related_id=proj2.id,
    tax_amount=1500.0,
    date=days_ago(2)
)

print("Data Population Complete!")
print("Please restart the server (uvicorn) if it was running, then check the Dashboard.")
