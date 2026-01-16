from fastapi.testclient import TestClient
from main import app
from db.storage import Storage
import os
import shutil

# Setup Test DB
TEST_DB = "test_phase4_data"
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)
from main import storage
storage.db_path = TEST_DB
if not os.path.exists(TEST_DB):
    os.makedirs(TEST_DB)

client = TestClient(app)

print("Starting Phase 4 Verification...")

# 1. Verify Flash Messages on Inventory Add
print("Testing Flash Message logic...")
response = client.post("/inventory/add", data={
    "type": "material",
    "name": "Test Wood",
    "unit_or_price": "m3",
    "cost": "100"
}, follow_redirects=False)
assert response.status_code == 303
assert "success_msg=Item+Added" in response.headers["location"]
print("Flash Message Redirect OK")

# 2. Verify Flash Message Display
response = client.get("/inventory?success_msg=Item+Added")
assert response.status_code == 200
assert "Item Added" in response.text
assert "flash-message success" in response.text
print("Flash Message Display OK")

# 3. Verify Mobile Header presence
response = client.get("/")
assert "mobile-header" in response.text
assert "menu-toggle" in response.text
print("Mobile Header OK")

# Cleanup
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)
print("Phase 4 Verification Complete!")
