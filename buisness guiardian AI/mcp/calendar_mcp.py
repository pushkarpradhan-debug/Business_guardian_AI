# MCP STUB — returns mock data for development/testing. Replace with real API calls in production.
"""Calendar MCP Client Stub."""

from __future__ import annotations
from datetime import datetime, timezone, timedelta
import re
from typing import Any

def fetch_calendar_data(inputs: dict[str, Any]) -> dict[str, Any]:
    """Validate input parameters and retrieve corporate compliance deadlines.
    
    Conforms to v1.1 API_CONTRACTS response envelope.
    """
    calendar_id = inputs.get("calendar_id")
    look_ahead_days = inputs.get("look_ahead_days")
    event_types = inputs.get("event_types", [])
    
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    try:
        # 1. Validation: calendar_id must be non-empty
        if not calendar_id or not isinstance(calendar_id, str):
            return {
                "mcp": "calendar_mcp",
                "status": "error",
                "error_code": "MISSING_CALENDAR_ID",
                "error_message": "calendar_id is a required configuration parameter and must be non-empty.",
                "fetched_at": fetched_at
            }
            
        # 2. Validation: look_ahead_days range checks
        if look_ahead_days is None:
            return {
                "mcp": "calendar_mcp",
                "status": "error",
                "error_code": "INVALID_LOOK_AHEAD_DAYS",
                "error_message": "look_ahead_days is required.",
                "fetched_at": fetched_at
            }
            
        try:
            look_ahead_days = int(look_ahead_days)
            if not (1 <= look_ahead_days <= 365):
                raise ValueError()
        except (ValueError, TypeError):
            return {
                "mcp": "calendar_mcp",
                "status": "error",
                "error_code": "INVALID_LOOK_AHEAD_DAYS",
                "error_message": "look_ahead_days must be an integer between 1 and 365.",
                "fetched_at": fetched_at
            }
            
        # 3. Validation: event_types checklist
        permitted_types = ["tax", "license", "insurance", "regulatory", "contract_renewal", "other"]
        if event_types is not None:
            if not isinstance(event_types, list):
                return {
                    "mcp": "calendar_mcp",
                    "status": "error",
                    "error_code": "INVALID_EVENT_TYPE",
                    "error_message": "event_types must be a list of strings.",
                    "fetched_at": fetched_at
                }
            for et in event_types:
                if et not in permitted_types:
                    return {
                        "mcp": "calendar_mcp",
                        "status": "error",
                        "error_code": "INVALID_EVENT_TYPE",
                        "error_message": f"Event type '{et}' is not a valid compliance category.",
                        "fetched_at": fetched_at
                    }
                    
        # Mock compliance calendar events
        all_events = [
            {
                "event_id": "EVT-001",
                "event_name": "Quarterly GST Filing Q2",
                "event_type": "tax",
                "due_date": "2026-07-15",
                "description": "GST tax return filing obligation for Q2 operational revenue.",
                "responsible_party": "finance_manager",
                "status": "pending",
                "recurrence": "quarterly"
            },
            {
                "event_id": "EVT-002",
                "event_name": "Corporate Insurance Policy Renewal",
                "event_type": "insurance",
                "due_date": "2026-07-28",
                "description": "Commercial general liability policy renewal deadline.",
                "responsible_party": "ops_director",
                "status": "pending",
                "recurrence": "annual"
            },
            {
                "event_id": "EVT-003",
                "event_name": "Municipal Food Safety License Renewal",
                "event_type": "license",
                "due_date": "2026-06-20",  # Overdue relative to current date (2026-06-26)
                "description": "Annual food production safety audit and certification renewal.",
                "responsible_party": "compliance_lead",
                "status": "overdue",
                "recurrence": "annual"
            }
        ]
        
        # 4. Perform integrity check on the event dates
        for e in all_events:
            due_date = e.get("due_date")
            if not due_date or not isinstance(due_date, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", due_date):
                return {
                    "mcp": "calendar_mcp",
                    "status": "error",
                    "error_code": "INVALID_DATE_FORMAT",
                    "error_message": f"Calendar event '{e.get('event_id')}' contains a malformed date string.",
                    "fetched_at": fetched_at
                }
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                return {
                    "mcp": "calendar_mcp",
                    "status": "error",
                    "error_code": "INVALID_DATE_FORMAT",
                    "error_message": f"Calendar event '{e.get('event_id')}' contains an invalid calendar date.",
                    "fetched_at": fetched_at
                }
                
        # 5. Filter events by look-ahead window and type
        now = datetime.now(timezone.utc)
        current_date_str = now.strftime("%Y-%m-%d")
        limit_date_str = (now + timedelta(days=look_ahead_days)).strftime("%Y-%m-%d")
        
        filtered_events = []
        for e in all_events:
            # Match type filter if specified
            if event_types and e["event_type"] not in event_types:
                continue
                
            due_date = e["due_date"]
            # Include if overdue (in the past) or within the look-ahead window
            if due_date < current_date_str or (current_date_str <= due_date <= limit_date_str):
                filtered_events.append(e)
                
        return {
            "mcp": "calendar_mcp",
            "status": "success",
            "data": {
                "calendar_events": filtered_events,
                "look_ahead_days": look_ahead_days,
                "total_events_returned": len(filtered_events)
            },
            "warnings": None,
            "fetched_at": fetched_at
        }
        
    except Exception as e:
        return {
            "mcp": "calendar_mcp",
            "status": "error",
            "error_code": "FETCH_FAILED",
            "error_message": f"An unexpected error occurred while fetching calendar data: {str(e)}",
            "fetched_at": fetched_at
        }
