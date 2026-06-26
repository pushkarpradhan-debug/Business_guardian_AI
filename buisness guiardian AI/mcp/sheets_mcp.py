# MCP STUB — returns mock data for development/testing. Replace with real API calls in production.
"""Google Sheets MCP Client Stub."""

from __future__ import annotations
from datetime import datetime, timezone
import re
from typing import Any

def get_inventory_data(spreadsheet_id: str | None = None) -> list[dict[str, Any]]:
    """Helper to return realistic mock inventory records."""
    return [
        {
            "inventory_id": "INV-001",
            "product_id": "PROD-001",
            "current_stock": 50,
            "warehouse_location": "Warehouse Zone A",
            "last_updated": "2026-06-25T12:00:00Z",
            "recorded_by": "google_sheets_mcp"
        },
        {
            "inventory_id": "INV-002",
            "product_id": "PROD-002",
            "current_stock": 3,
            "warehouse_location": "Warehouse Zone B",
            "last_updated": "2026-06-25T14:30:00Z",
            "recorded_by": "google_sheets_mcp"
        },
        {
            "inventory_id": "INV-003",
            "product_id": "PROD-003",
            "current_stock": 12,
            "warehouse_location": "Warehouse Zone A",
            "last_updated": "2026-06-25T09:15:00Z",
            "recorded_by": "google_sheets_mcp"
        }
    ]

def get_sales_data(spreadsheet_id: str | None = None, days: int = 30) -> list[dict[str, Any]]:
    """Helper to return realistic mock sales records."""
    return [
        {
            "sale_id": "SALE-001",
            "product_id": "PROD-001",
            "quantity_sold": 15,
            "sale_amount": 300.0,
            "unit_price_at_sale": 20.0,
            "sale_date": "2026-06-10",
            "channel": "online",
            "recorded_at": "2026-06-10T15:00:00Z"
        },
        {
            "sale_id": "SALE-002",
            "product_id": "PROD-002",
            "quantity_sold": 8,
            "sale_amount": 120.0,
            "unit_price_at_sale": 15.0,
            "sale_date": "2026-06-12",
            "channel": "in_store",
            "recorded_at": "2026-06-12T16:00:00Z"
        },
        {
            "sale_id": "SALE-003",
            "product_id": "PROD-003",
            "quantity_sold": 5,
            "sale_amount": 250.0,
            "unit_price_at_sale": 50.0,
            "sale_date": "2026-06-15",
            "channel": "online",
            "recorded_at": "2026-06-15T10:00:00Z"
        },
        {
            "sale_id": "SALE-004",
            "product_id": "PROD-001",
            "quantity_sold": 20,
            "sale_amount": 400.0,
            "unit_price_at_sale": 20.0,
            "sale_date": "2026-06-20",
            "channel": "wholesale",
            "recorded_at": "2026-06-20T11:00:00Z"
        },
        {
            "sale_id": "SALE-005",
            "product_id": "PROD-002",
            "quantity_sold": 14,
            "sale_amount": 210.0,
            "unit_price_at_sale": 15.0,
            "sale_date": "2026-06-22",
            "channel": "online",
            "recorded_at": "2026-06-22T17:30:00Z"
        }
    ]

def get_expenses_data(spreadsheet_id: str | None = None, days: int = 30) -> list[dict[str, Any]]:
    """Helper to return realistic mock expense records."""
    return [
        {
            "expense_id": "EXP-001",
            "expense_category": "rent",
            "amount": 800.0,
            "description": "Office sublease monthly rent",
            "expense_date": "2026-06-01",
            "vendor": "Prime Real Estate",
            "recorded_at": "2026-06-01T08:00:00Z"
        },
        {
            "expense_id": "EXP-002",
            "expense_category": "utilities",
            "amount": 150.0,
            "description": "Monthly energy and water bill",
            "expense_date": "2026-06-10",
            "vendor": "Central Energy Grid",
            "recorded_at": "2026-06-10T09:30:00Z"
        },
        {
            "expense_id": "EXP-003",
            "expense_category": "inventory",
            "amount": 450.0,
            "description": "Supplier restock shipment",
            "expense_date": "2026-06-14",
            "vendor": "Alpha Supplies",
            "recorded_at": "2026-06-14T11:45:00Z"
        }
    ]

def get_suppliers_data(spreadsheet_id: str | None = None) -> list[dict[str, Any]]:
    """Helper to return realistic mock supplier records."""
    return [
        {
            "supplier_id": "SUP-001",
            "supplier_name": "Alpha Supplies",
            "contact_name": "John Doe",
            "contact_email": "john@alphasupplies.com",
            "country": "USA",
            "product_categories": ["electronics", "office_supplies"],
            "dependency_percentage": 75.0,
            "contract_start_date": "2026-01-01",
            "contract_end_date": "2026-12-31",
            "is_active": True,
            "created_at": "2026-01-01T00:00:00Z"
        },
        {
            "supplier_id": "SUP-002",
            "supplier_name": "Beta Logistics",
            "contact_name": "Jane Smith",
            "contact_email": "jane@betalogistics.com",
            "country": "Canada",
            "product_categories": ["packaging", "delivery_services"],
            "dependency_percentage": 25.0,
            "contract_start_date": "2026-02-01",
            "contract_end_date": "2026-11-30",
            "is_active": True,
            "created_at": "2026-02-01T00:00:00Z"
        }
    ]

def validate_inventory_record(record: dict[str, Any]) -> str | None:
    """Validate a single inventory record according to API_CONTRACTS.md.
    
    Returns error code if invalid, else None.
    """
    required_fields = ["inventory_id", "product_id", "current_stock", "last_updated", "recorded_by"]
    for field in required_fields:
        if field not in record or record[field] is None or record[field] == "":
            return "MISSING_REQUIRED_FIELD"
            
    current_stock = record["current_stock"]
    if not isinstance(current_stock, int):
        try:
            current_stock = int(current_stock)
        except (ValueError, TypeError):
            return "MISSING_REQUIRED_FIELD"
            
    if current_stock < 0:
        return "NEGATIVE_STOCK_VALUE"
        
    return None

def validate_sales_record(record: dict[str, Any]) -> str | None:
    """Validate a single sales record according to API_CONTRACTS.md.
    
    Returns error code if invalid, else None.
    """
    required_fields = ["sale_id", "product_id", "quantity_sold", "sale_amount", "unit_price_at_sale", "sale_date", "recorded_at"]
    for field in required_fields:
        if field not in record or record[field] is None or record[field] == "":
            return "MISSING_REQUIRED_FIELD"
            
    quantity_sold = record["quantity_sold"]
    if not isinstance(quantity_sold, int):
        try:
            quantity_sold = int(quantity_sold)
        except (ValueError, TypeError):
            return "MISSING_REQUIRED_FIELD"
            
    if quantity_sold <= 0:
        return "INVALID_QUANTITY_VALUE"
        
    for field in ["sale_amount", "unit_price_at_sale"]:
        val = record[field]
        if not isinstance(val, (int, float)):
            try:
                val = float(val)
            except (ValueError, TypeError):
                return "MISSING_REQUIRED_FIELD"
        if val < 0.0:
            return "NEGATIVE_MONETARY_VALUE"
            
    return None

def validate_expense_record(record: dict[str, Any]) -> str | None:
    """Validate a single expense record according to API_CONTRACTS.md.
    
    Returns error code if invalid, else None.
    """
    required_fields = ["expense_id", "expense_category", "amount", "expense_date", "recorded_at"]
    for field in required_fields:
        if field not in record or record[field] is None or record[field] == "":
            return "MISSING_REQUIRED_FIELD"
            
    amount = record["amount"]
    if not isinstance(amount, (int, float)):
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return "MISSING_REQUIRED_FIELD"
            
    if amount < 0.0:
        return "NEGATIVE_MONETARY_VALUE"
        
    return None

def validate_supplier_record(record: dict[str, Any]) -> str | None:
    """Validate a single supplier record according to API_CONTRACTS.md.
    
    Returns error code if invalid, else None.
    """
    required_fields = ["supplier_id", "supplier_name", "country", "product_categories", "is_active", "created_at"]
    for field in required_fields:
        if field not in record or record[field] is None or (field != "product_categories" and record[field] == ""):
            return "MISSING_REQUIRED_FIELD"
            
    if not isinstance(record["product_categories"], list):
        return "MISSING_REQUIRED_FIELD"
        
    dependency_percentage = record.get("dependency_percentage")
    if dependency_percentage is not None:
        if not isinstance(dependency_percentage, (int, float)):
            try:
                dependency_percentage = float(dependency_percentage)
            except (ValueError, TypeError):
                return "MISSING_REQUIRED_FIELD"
        if dependency_percentage < 0.0 or dependency_percentage > 100.0:
            return "INVALID_PERCENTAGE_VALUE"
            
    return None

def _get_error_message(error_code: str) -> str:
    """Map validation error codes to human-readable error messages."""
    messages = {
        "MISSING_REQUIRED_FIELD": "Mandatory cell is empty or has invalid type in sheet.",
        "NEGATIVE_STOCK_VALUE": "Inventory record contains negative current_stock.",
        "INVALID_QUANTITY_VALUE": "Sales record contains zero or negative quantity_sold.",
        "NEGATIVE_MONETARY_VALUE": "Sales or expense record contains negative monetary amount.",
        "INVALID_PERCENTAGE_VALUE": "Supplier record contains dependency_percentage < 0 or > 100."
    }
    return messages.get(error_code, "Validation error occurred.")

def fetch_sheets_data(inputs: dict[str, Any]) -> dict[str, Any]:
    """Validate and fetch data from mock Google Sheets.
    
    Conforms to v1.1 API_CONTRACTS response envelope.
    """
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    try:
        spreadsheet_id = inputs.get("spreadsheet_id")
        sheets = inputs.get("sheets")
        date_range = inputs.get("date_range")
        
        # 1. Validation: spreadsheet_id must be non-empty
        if not spreadsheet_id or not isinstance(spreadsheet_id, str):
            return {
                "mcp": "google_sheets_mcp",
                "status": "error",
                "error_code": "MISSING_SPREADSHEET_ID",
                "error_message": "spreadsheet_id must be a non-empty string.",
                "fetched_at": fetched_at
            }
            
        # 2. Validation: sheets must be non-empty and valid
        if not sheets or not isinstance(sheets, list):
            return {
                "mcp": "google_sheets_mcp",
                "status": "error",
                "error_code": "INVALID_SHEET_NAME",
                "error_message": "sheets must be a non-empty list.",
                "fetched_at": fetched_at
            }
            
        for sheet in sheets:
            if sheet not in ["inventory", "sales", "expenses", "suppliers"]:
                return {
                    "mcp": "google_sheets_mcp",
                    "status": "error",
                    "error_code": "INVALID_SHEET_NAME",
                    "error_message": f"Sheet '{sheet}' is not a recognized operational data tab.",
                    "fetched_at": fetched_at
                }
                
        # 3. Validation: date format check YYYY-MM-DD
        if not isinstance(date_range, dict) or "start_date" not in date_range or "end_date" not in date_range:
            return {
                "mcp": "google_sheets_mcp",
                "status": "error",
                "error_code": "INVALID_DATE_FORMAT",
                "error_message": "date_range must be a dictionary containing 'start_date' and 'end_date'.",
                "fetched_at": fetched_at
            }
            
        start_date = date_range["start_date"]
        end_date = date_range["end_date"]
        
        date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not isinstance(start_date, str) or not isinstance(end_date, str) or not date_regex.match(start_date) or not date_regex.match(end_date):
            return {
                "mcp": "google_sheets_mcp",
                "status": "error",
                "error_code": "INVALID_DATE_FORMAT",
                "error_message": "start_date and end_date must be formatted as YYYY-MM-DD.",
                "fetched_at": fetched_at
            }
            
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {
                "mcp": "google_sheets_mcp",
                "status": "error",
                "error_code": "INVALID_DATE_FORMAT",
                "error_message": "start_date or end_date is not a valid calendar date.",
                "fetched_at": fetched_at
            }
            
        # 4. Validation: date chronological order check
        if end_dt < start_dt:
            return {
                "mcp": "google_sheets_mcp",
                "status": "error",
                "error_code": "INVALID_DATE_RANGE",
                "error_message": "end_date must be chronologically on or after start_date.",
                "fetched_at": fetched_at
            }
            
        # Build data payload
        data: dict[str, Any] = {}
        
        # Load sheets data and perform integrity checks
        if "inventory" in sheets:
            inventory_records = get_inventory_data(spreadsheet_id)
            for record in inventory_records:
                error_code = validate_inventory_record(record)
                if error_code:
                    return {
                        "mcp": "google_sheets_mcp",
                        "status": "error",
                        "error_code": error_code,
                        "error_message": _get_error_message(error_code),
                        "fetched_at": fetched_at
                    }
            data["inventory"] = inventory_records
            
        if "sales" in sheets:
            sales_records = get_sales_data(spreadsheet_id)
            filtered_sales = []
            for record in sales_records:
                error_code = validate_sales_record(record)
                if error_code:
                    return {
                        "mcp": "google_sheets_mcp",
                        "status": "error",
                        "error_code": error_code,
                        "error_message": _get_error_message(error_code),
                        "fetched_at": fetched_at
                    }
                # Filter sales by date range
                sale_date = record["sale_date"]
                if start_date <= sale_date <= end_date:
                    filtered_sales.append(record)
            data["sales"] = filtered_sales
            
        if "expenses" in sheets:
            expenses_records = get_expenses_data(spreadsheet_id)
            filtered_expenses = []
            for record in expenses_records:
                error_code = validate_expense_record(record)
                if error_code:
                    return {
                        "mcp": "google_sheets_mcp",
                        "status": "error",
                        "error_code": error_code,
                        "error_message": _get_error_message(error_code),
                        "fetched_at": fetched_at
                    }
                # Filter expenses by date range
                expense_date = record["expense_date"]
                if start_date <= expense_date <= end_date:
                    filtered_expenses.append(record)
            data["expenses"] = filtered_expenses
            
        if "suppliers" in sheets:
            suppliers_records = get_suppliers_data(spreadsheet_id)
            for record in suppliers_records:
                error_code = validate_supplier_record(record)
                if error_code:
                    return {
                        "mcp": "google_sheets_mcp",
                        "status": "error",
                        "error_code": error_code,
                        "error_message": _get_error_message(error_code),
                        "fetched_at": fetched_at
                    }
            data["suppliers"] = suppliers_records
            
        return {
            "mcp": "google_sheets_mcp",
            "status": "success",
            "data": data,
            "warnings": None,
            "fetched_at": fetched_at
        }
        
    except Exception as e:
        return {
            "mcp": "google_sheets_mcp",
            "status": "error",
            "error_code": "FETCH_FAILED",
            "error_message": f"An unexpected error occurred while fetching sheets data: {str(e)}",
            "fetched_at": fetched_at
        }
