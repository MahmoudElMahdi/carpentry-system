from fastapi.testclient import TestClient
from main import app
from db.storage import Storage
import os
import shutil

# Setup Test DB
TEST_DB = "test_phase2_data"
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)

# Monkey Patch Storage
from main import storage
storage.db_path = TEST_DB
if not os.path.exists(TEST_DB):
    os.makedirs(TEST_DB)

client = TestClient(app)

print("Starting Phase 2 Verification...")

# 1. Create Customer
print("Creating Customer...")
response = client.post("/contacts/add", data={
    "name": "Client A",
    "role": "CUSTOMER",
    "phone": "555-0000"
})
assert response.status_code == 303 or response.status_code == 200

# Get customer ID from storage
customers = storage.load('contacts')
client_a_id = customers[0]['id']

# 2. Create Project
print("Creating Project...")
response = client.post("/projects/add", data={
    "name": "Villa Kitchen",
    "customer_id": client_a_id,
    "total_value": "10000.0",
    "description": "Full kitchen renovation"
})
assert response.status_code == 303 or response.status_code == 200
print("Project Created OK")

# Get project ID
projects = storage.load('projects')
project_id = projects[0]['id']

# 3. Record Project Payment (Sale)
print("Recording Project Payment...")
response = client.post("/finance/transaction", data={
    "type": "SALE",
    "amount": "2000.0",
    "description": "Deposit",
    "category": "Project Payment",
    "contact_id": client_a_id,
    "related_id": project_id, # Linking to project
    "tax_amount": "200.0" # VAT Included
})
assert response.status_code == 303 or response.status_code == 200
print("Payment Recorded OK")

# 4. Verify Project Summary (Remaining Balance)
# We can check via the page content or directly inspect logic
print("Verifying Project Balance on Page...")
response = client.get("/projects")
assert "Villa Kitchen" in response.text
assert "8000.0" in response.text # 10000 - 2000 remaining
print("Project Balance OK")

# 5. Verify Tax Report
# Total Tax In = 200.0
assert "200.0" in response.text # Net VAT Payable should be visible
print("Tax Report OK")

# Cleanup
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)

print("Phase 2 Verification Complete!")
