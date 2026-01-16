from fastapi.testclient import TestClient
from main import app
from db.storage import Storage
from services.finance_service import FinanceService
import os
import shutil

# Setup Test DB
TEST_DB = "test_phase3_data"
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)

# Monkey Patch
from main import storage
storage.db_path = TEST_DB
if not os.path.exists(TEST_DB):
    os.makedirs(TEST_DB)

client = TestClient(app)
finance_service = FinanceService(storage)

print("Starting Phase 3 Verification...")

# 1. Setup Data: 1 Sale (1000), 1 Expense (500), 1 Payroll (200)
# Sale: Cash, Company Source
finance_service.record_transaction("SALE", 1000.0, "S1", payment_source="Company", date="2025-01-01")
# Expense: Rent, Company Source
finance_service.record_transaction("EXPENSE", 500.0, "E1", category="Rent", payment_source="Company", date="2025-01-02")
# Payroll: Salary, Company Source
finance_service.record_transaction("PAYROLL", 200.0, "P1", category="Payroll", payment_source="Company", date="2025-01-03")

# 2. Verify Formulas via Service
print("Verifying Formulas...")
summary = finance_service.get_financial_summary()
assert summary['total_revenue'] == 1000.0
assert summary['total_expenses'] == 700.0 # 500 + 200
assert summary['net_profit'] == 300.0 # 1000 - 700
assert summary['cash_on_hand'] == 300.0
print("Formulas OK")

# 3. Verify Monthly Trends
print("Verifying Monthly Trends...")
# Note: Manually setting date in record_transaction might not work if the service overrides it with datetime.now()
# Checking the service implementation: It assumes `Transaction` defaults date to now, but record_transaction doesn't accept date arg in previous impl.
# We need to manually fix the dates in storage for this test to calculate monthly trends correctly
transactions = storage.load('transactions')
# Check for '2025-01' as we injected that date
target_month = "2025-01"

trends = finance_service.get_monthly_trends()
assert target_month in trends['labels']
idx = trends['labels'].index(target_month)
assert trends['income'][idx] == 1000.0
assert trends['expense'][idx] == 700.0
print("Monthly Trends OK")

# 4. Verify Dashboard Page Load
print("Verifying Dashboard Page...")
response = client.get("/")
assert response.status_code == 200
assert "300.0" in response.text # Net Profit
assert "Chart" in response.text # JS Chart present
print("Dashboard Page OK")

# Cleanup
if os.path.exists(TEST_DB):
    shutil.rmtree(TEST_DB)

print("Phase 3 Verification Complete!")
