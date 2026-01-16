from services.inventory_service import InventoryService
from services.finance_service import FinanceService
from db.storage import Storage
import os
import shutil

# Use a test directory for storage to avoid messing up real data
TEST_DB = "test_data"
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)

storage = Storage(db_path=TEST_DB)
inventory = InventoryService(storage)
finance = FinanceService(storage)

print("Testing Inventory Service...")
m1 = inventory.add_material("Wood", "m3", 100.0)
p1 = inventory.add_product("Table", 250.0)
assert len(inventory.list_materials()) == 1
assert len(inventory.list_products()) == 1
print("Inventory Service OK")

print("Testing Finance Service...")
finance.record_transaction("EXPENSE", 1000.0, "Initial Investment")
finance.record_transaction("SALE", 500.0, "First Sale")
balance = finance.get_balance()
assert balance == -500.0
print(f"Finance Service OK. Balance: {balance}")

# Cleanup
# shutil.rmtree(TEST_DB)  # Keep it for inspection if needed, or remove
print("All tests passed!")
