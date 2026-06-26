# MCP STUB — returns mock data for development/testing. Replace with real API calls in production.
"""Supplier Intelligence MCP Client Stub."""

from __future__ import annotations
from datetime import datetime, timezone
import re
from typing import Any

def _is_valid_date(date_str: Any) -> bool:
    """Check if date_str is formatted as YYYY-MM-DD and is a valid calendar date."""
    if not isinstance(date_str, str):
        return False
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def _is_valid_month(month_str: Any) -> bool:
    """Check if month_str is formatted as YYYY-MM and is a valid calendar month."""
    if not isinstance(month_str, str):
        return False
    if not re.match(r"^\d{4}-\d{2}$", month_str):
        return False
    try:
        datetime.strptime(month_str, "%Y-%m")
        return True
    except ValueError:
        return False

def fetch_supplier_intelligence(inputs: dict[str, Any]) -> dict[str, Any]:
    """Validate supplier IDs and fetch delivery performance, profiles, and risk markers.
    
    Conforms to v1.1 API_CONTRACTS response envelope.
    """
    supplier_ids = inputs.get("supplier_ids", [])
    include_history = inputs.get("include_history", True)
    history_months = inputs.get("history_months", 6)
    
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    try:
        # 1. Validation: supplier_ids array checks
        if not supplier_ids or not isinstance(supplier_ids, list):
            return {
                "mcp": "supplier_intelligence_mcp",
                "status": "error",
                "error_code": "MISSING_SUPPLIER_IDS",
                "error_message": "supplier_ids list must be provided and must be non-empty.",
                "fetched_at": fetched_at
            }
            
        for s_id in supplier_ids:
            if not isinstance(s_id, str) or not s_id:
                return {
                    "mcp": "supplier_intelligence_mcp",
                    "status": "error",
                    "error_code": "MISSING_SUPPLIER_IDS",
                    "error_message": "supplier_ids must contain only non-empty strings.",
                    "fetched_at": fetched_at
                }
                
        # 2. Validation: history_months checks
        try:
            history_months = int(history_months)
            if not (1 <= history_months <= 24):
                raise ValueError()
        except (ValueError, TypeError):
            return {
                "mcp": "supplier_intelligence_mcp",
                "status": "error",
                "error_code": "INVALID_HISTORY_MONTHS",
                "error_message": "history_months must be an integer between 1 and 24.",
                "fetched_at": fetched_at
            }
            
        # Mock supplier intelligence databases
        profiles_db = {
            "SUP-001": {
                "supplier_id": "SUP-001",
                "supplier_name": "Alpha Supplies",
                "country": "USA",
                "product_categories": ["electronics", "office_supplies"],
                "reliability_score": 85,
                "quality_score": 92,
                "delivery_performance": {
                    "on_time_rate_percent": 90.5,
                    "average_delay_days": 1.2
                },
                "financial_stability_indicator": "stable",
                "active_since": "2023-01-15",
                "contract_end_date": "2026-12-31",
                "risk_flags": []
            },
            "SUP-002": {
                "supplier_id": "SUP-002",
                "supplier_name": "Beta Logistics",
                "country": "Canada",
                "product_categories": ["packaging", "delivery_services"],
                "reliability_score": 58,  # Underperforming
                "quality_score": 75,
                "delivery_performance": {
                    "on_time_rate_percent": 68.0,
                    "average_delay_days": 4.5
                },
                "financial_stability_indicator": "watch",
                "active_since": "2024-03-10",
                "contract_end_date": "2026-11-30",
                "risk_flags": ["high_delay_rate", "financial_stability_watch"]
            }
        }
        
        history_db = {
            "SUP-001": [
                {
                    "supplier_id": "SUP-001",
                    "month": "2026-05",
                    "orders_placed": 10,
                    "orders_fulfilled": 10,
                    "fulfilment_rate_percent": 100.0,
                    "incidents": []
                },
                {
                    "supplier_id": "SUP-001",
                    "month": "2026-04",
                    "orders_placed": 12,
                    "orders_fulfilled": 11,
                    "fulfilment_rate_percent": 91.6,
                    "incidents": ["Damaged packaging on 1 parcel"]
                }
            ],
            "SUP-002": [
                {
                    "supplier_id": "SUP-002",
                    "month": "2026-05",
                    "orders_placed": 15,
                    "orders_fulfilled": 10,
                    "fulfilment_rate_percent": 66.6,
                    "incidents": ["Late delivery - 5 days delay"]
                },
                {
                    "supplier_id": "SUP-002",
                    "month": "2026-04",
                    "orders_placed": 8,
                    "orders_fulfilled": 5,
                    "fulfilment_rate_percent": 62.5,
                    "incidents": ["Incorrect items sent in order"]
                }
            ]
        }
        
        risk_db = {
            "SUP-001": {
                "supplier_id": "SUP-001",
                "risk_score": 15,
                "risk_level": "low",
                "primary_risk_factor": "none",
                "last_assessed": "2026-06-01"
            },
            "SUP-002": {
                "supplier_id": "SUP-002",
                "risk_score": 75,
                "risk_level": "high",
                "primary_risk_factor": "Fulfillment failure and high delays",
                "last_assessed": "2026-06-20"
            }
        }
        
        # 3. Perform domain checks on mock data before returning to prevent payload corruption
        permitted_indicators = ["stable", "watch", "at_risk"]
        permitted_levels = ["high", "medium", "low"]
        
        for key, p in profiles_db.items():
            if not _is_valid_date(p["active_since"]):
                raise ValueError(f"Supplier {key} contains invalid active_since date.")
            if p["contract_end_date"] is not None and not _is_valid_date(p["contract_end_date"]):
                raise ValueError(f"Supplier {key} contains invalid contract_end_date.")
            if p["financial_stability_indicator"] not in permitted_indicators:
                raise ValueError(f"Supplier {key} contains invalid stability indicator.")
            if not (0 <= p["reliability_score"] <= 100) or not (0 <= p["quality_score"] <= 100):
                raise ValueError(f"Supplier {key} contains score out of range.")
                
        for key, hist in history_db.items():
            for entry in hist:
                if not _is_valid_month(entry["month"]):
                    raise ValueError(f"Supplier history entry for {key} has invalid month format.")
                    
        for key, r in risk_db.items():
            if not _is_valid_date(r["last_assessed"]):
                raise ValueError(f"Supplier risk data for {key} has invalid last_assessed date.")
            if r["risk_level"] not in permitted_levels:
                raise ValueError(f"Supplier risk data for {key} has invalid risk level.")
            if not (0 <= r["risk_score"] <= 100):
                raise ValueError(f"Supplier risk data for {key} has risk score out of range.")
                
        # Resolve requested suppliers
        supplier_profiles = []
        supplier_history = []
        supplier_risk_data = []
        warnings = []
        
        for s_id in supplier_ids:
            if s_id in profiles_db:
                supplier_profiles.append(profiles_db[s_id])
                if include_history and s_id in history_db:
                    supplier_history.extend(history_db[s_id][:history_months])
                if s_id in risk_db:
                    supplier_risk_data.append(risk_db[s_id])
            else:
                warnings.append(f"Supplier ID '{s_id}' not found in intelligence database.")
                
        # Check if any supplier was resolved
        if not supplier_profiles:
            return {
                "mcp": "supplier_intelligence_mcp",
                "status": "error",
                "error_code": "NO_SUPPLIERS_FOUND",
                "error_message": "Zero requested supplier IDs resolved in the intelligence database.",
                "fetched_at": fetched_at
            }
            
        return {
            "mcp": "supplier_intelligence_mcp",
            "status": "success",
            "data": {
                "supplier_profiles": supplier_profiles,
                "supplier_history": supplier_history,
                "supplier_risk_data": supplier_risk_data,
                "total_suppliers_returned": len(supplier_profiles)
            },
            "warnings": warnings if warnings else None,
            "fetched_at": fetched_at
        }
        
    except ValueError as ve:
        return {
            "mcp": "supplier_intelligence_mcp",
            "status": "error",
            "error_code": "CORRUPTED_PAYLOAD_ERROR",
            "error_message": f"Database payload error: {str(ve)}",
            "fetched_at": fetched_at
        }
    except Exception as e:
        return {
            "mcp": "supplier_intelligence_mcp",
            "status": "error",
            "error_code": "UPSTREAM_API_TIMEOUT",
            "error_message": f"An unexpected error occurred while fetching supplier intelligence: {str(e)}",
            "fetched_at": fetched_at
        }
