from fastapi.testclient import TestClient
from main import app
from db.storage import Storage
import os
import shutil

# Setup Test DB
TEST_DB = "test_phase1_data"
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)

# Monkey Patch Storage
# (Note: In a real app we'd use dependency injection overrides)
from main import storage
storage.db_path = TEST_DB
if not os.path.exists(TEST_DB):
    os.makedirs(TEST_DB)

client = TestClient(app)

print("Starting Phase 1 Verification...")

# 1. Add Contact (Supplier)
print("Testing Add Contact...")
response = client.post("/contacts/add", data={
    "name": "Supplier X",
    "role": "SUPPLIER",
    "phone": "123456789"
})
assert response.status_code == 303 or response.status_code == 200
print("Contact Added OK")

# 2. Get Contacts List (verify internal storage)
contacts = storage.load('contacts')
assert len(contacts) == 1
assert contacts[0]['name'] == "Supplier X"
supplier_id = contacts[0]['id']

# 3. Record Purchase (Unified Input)
print("Testing Unified Purchase Input...")
response = client.post("/finance/transaction", data={
    "type": "PURCHASE",
    "amount": "5000.0",
    "description": "Wood Purchase",
    "category": "Raw Materials",
    "payment_method": "Cash",
    "payment_source": "Company",
    "tax_amount": "500.0",
    "contact_id": supplier_id
})
assert response.status_code == 303 or response.status_code == 200
print("Purchase Recorded OK")

# 4. Record Payroll (Expense)
print("Testing Payroll Input...")
response = client.post("/finance/transaction", data={
    "type": "PAYROLL",
    "amount": "2000.0",
    "description": "Worker Salary",
    "category": "Salary",
    "payment_method": "Cash",
    "payment_source": "Company",
    "tax_amount": "0.0"
})
assert response.status_code == 303 or response.status_code == 200
print("Payroll Recorded OK")

# 5. Verify Finance List (Page Load)
print("Testing Finance Page Load...")
response = client.get("/finance")
assert response.status_code == 200
assert "Wood Purchase" in response.text
assert "Supplier X" in response.text
assert "Worker Salary" in response.text
print("Finance Page Verification OK")

# Cleanup
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)

print("Phase 1 Verification Complete!")
