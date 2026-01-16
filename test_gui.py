from fastapi.testclient import TestClient
from main import app
from db.storage import Storage
import os
import shutil

# Use a test DB
TEST_DB = "test_gui_data"
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)

# Monkey patch storage in the app dependencies if possible, 
# but main.py initializes global services. Ideally we'd override dependencies.
# For now, we'll swap the storage path for the global services by modifying the object 
# (Not robust for production but okay for this simple verification)
from main import storage, inventory_service, finance_service
storage.db_path = TEST_DB
storage._get_file_path = lambda x: os.path.join(TEST_DB, f"{x}.json")  # Re-bind logic if needed, but instance method uses self.db_path
if not os.path.exists(TEST_DB):
    os.makedirs(TEST_DB)

client = TestClient(app)

print("Testing Dashboard Endpoint...")
response = client.get("/")
assert response.status_code == 200
assert "CarpentrySys" in response.text
print("Dashboard OK")

print("Testing Inventory Endpoint...")
response = client.get("/inventory")
assert response.status_code == 200
print("Inventory Page OK")

print("Testing Transaction Record...")
response = client.post("/finance/transaction", data={
    "type": "SALE",
    "amount": "150.0",
    "description": "Test Sale GUI"
})
# Should redirect
assert response.status_code == 303 or response.status_code == 200 # Starlette might be 307/303
print("Transaction Record OK")

print("Verifying Balance Update...")
response = client.get("/finance")
assert "150.0" in response.text
print("Balance Update Verified")

# Cleanup
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)
    
print("All GUI Tests Passed!")
