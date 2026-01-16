from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from db.storage import Storage
from services.inventory_service import InventoryService
from services.finance_service import FinanceService
from services.sales_service import SalesService
import uvicorn

app = FastAPI()

# Setup Services
import os
db_path = os.getenv("DB_PATH", "data")  # Use /data on Render, data locally
storage = Storage(db_path=db_path)
inventory_service = InventoryService(storage)
finance_service = FinanceService(storage)
sales_service = SalesService(storage)

# Setup Templates and Static
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, success_msg: str = None):
    summary = finance_service.get_financial_summary()
    trends = finance_service.get_monthly_trends()
    expense_breakdown = finance_service.get_expense_breakdown()
    
    # Get last 5 transactions
    all_transactions = [t for t in finance_service.storage.load('transactions')]
    recent_transactions = sorted(all_transactions, key=lambda x: x['date'], reverse=True)[:5]

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "summary": summary,
        "trends": trends,
        "expense_breakdown": expense_breakdown,
        "recent_transactions": recent_transactions,
        "success_msg": success_msg
    })

@app.get("/inventory", response_class=HTMLResponse)
async def inventory_page(request: Request, success_msg: str = None):
    materials = inventory_service.list_materials()
    products = inventory_service.list_products()
    return templates.TemplateResponse("inventory.html", {
        "request": request,
        "materials": materials,
        "products": products,
        "success_msg": success_msg
    })

@app.post("/inventory/add")
async def add_inventory(
    type: str = Form(...),
    name: str = Form(...),
    unit_or_price: str = Form(...),
    cost: str = Form(None)
):
    if type == "material":
        cost_val = float(cost) if cost else 0.0
        inventory_service.add_material(name, unit_or_price, cost_val)
    elif type == "product":
        price_val = float(unit_or_price)
        inventory_service.add_product(name, price_val)
    
    return RedirectResponse(url="/inventory?success_msg=Item+Added", status_code=303)

@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request, success_msg: str = None):
    # Get all active projects with summary
    projects = sales_service.list_projects()
    summaries = [sales_service.get_project_summary(p.id) for p in projects]
    tax_report = sales_service.get_tax_report()
    customers = finance_service.list_contacts(role="CUSTOMER")
    
    return templates.TemplateResponse("projects.html", {
        "request": request,
        "project_summaries": summaries,
        "tax_report": tax_report,
        "active_projects_count": len(projects),
        "customers": customers,
        "success_msg": success_msg
    })

@app.post("/projects/add")
async def add_project(
    name: str = Form(...),
    customer_id: str = Form(...),
    total_value: float = Form(...),
    description: str = Form("")
):
    sales_service.create_project(name, customer_id, total_value, description)
    return RedirectResponse(url="/projects?success_msg=Project+Created", status_code=303)

@app.get("/finance", response_class=HTMLResponse)
async def finance_page(request: Request, success_msg: str = None):
    balance = finance_service.get_balance()
    # Load recent transactions for the table (limited to last 50 for now)
    # Using private method or direct storage access for simplicity or add method to service
    all_transactions = [t for t in finance_service.storage.load('transactions')]
    all_transactions.reverse() # Newest first
    contacts = finance_service.list_contacts()
    
    return templates.TemplateResponse("finance.html", {
        "request": request,
        "balance": balance,
        "transactions": all_transactions,
        "contacts": contacts,
        "success_msg": success_msg
    })

@app.post("/finance/transaction")
async def add_transaction(
    type: str = Form(...),
    amount: float = Form(...),
    description: str = Form(...),
    category: str = Form("General"),
    payment_method: str = Form("Cash"),
    payment_source: str = Form("Company"),
    tax_amount: str = Form("0.0"),
    contact_id: str = Form(None),
    related_id: str = Form(None)
):
    finance_service.record_transaction(
        type=type,
        amount=amount,
        description=description,
        category=category,
        payment_method=payment_method,
        payment_source=payment_source,
        tax_amount=float(tax_amount),
        contact_id=contact_id,
        related_id=related_id
    )
    return RedirectResponse(url="/finance?success_msg=Transaction+Recorded", status_code=303)

@app.post("/contacts/add")
async def add_contact(
    name: str = Form(...),
    role: str = Form(...),
    phone: str = Form("")
):
    finance_service.add_contact(name, role, phone)
    return RedirectResponse(url="/finance?success_msg=Contact+Added", status_code=303)
