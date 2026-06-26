"""Centralized configuration module for Business Guardian AI.

Loads all environment variables from a .env file via python-dotenv.
Every secret, path, and tunable constant is defined here.
No other module in the project should call os.getenv() directly.

Reference documents:
    - PROJECT_CONSTITUTION.md §6 (Coding Standards)
    - ORCHESTRATOR_CONTRACT.md §3.4 (Configuration Settings)
    - ORCHESTRATOR_CONTRACT.md §3.5 (Guardrail Policies)
    - API_CONTRACTS.md §Security Requirements
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from the project root (same directory as this file).
# override=False ensures real environment variables take precedence.
# ---------------------------------------------------------------------------
_PROJECT_ROOT: Path = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_PROJECT_ROOT / ".env", override=False)

# ===================================================================
# 1. DATABASE
# ===================================================================
# SQLite database file path.  Defaults to a file in the project root.
# Constitution §5: SQLite is the only permitted database engine in V1.
DB_PATH: str = os.getenv("DB_PATH", str(_PROJECT_ROOT / "business_guardian.db"))

# ===================================================================
# 2. GOOGLE SHEETS MCP
# ===================================================================
# API_CONTRACTS §1 — Google Sheets document ID.
# Must be loaded from environment; never hard-coded.
SPREADSHEET_ID: str = os.getenv("SPREADSHEET_ID", "")

# ===================================================================
# 3. CALENDAR MCP
# ===================================================================
# API_CONTRACTS §2 — Corporate calendar identifier.
CALENDAR_ID: str = os.getenv("CALENDAR_ID", "")

# ===================================================================
# 4. NEWS MCP
# ===================================================================
# API_CONTRACTS §3 — Controls for the news aggregation feed.
# max_articles_per_topic must be 1–25; max_age_days must be 1–90.
NEWS_MAX_ARTICLES: int = int(os.getenv("NEWS_MAX_ARTICLES", "5"))
NEWS_MAX_AGE_DAYS: int = int(os.getenv("NEWS_MAX_AGE_DAYS", "30"))

# ===================================================================
# 5. RISK REGISTRY MCP
# ===================================================================
# API_CONTRACTS §5 — Look-back window for historical risk scores.
# history_days must be 1–365; defaults to 90.
RISK_HISTORY_DAYS: int = int(os.getenv("RISK_HISTORY_DAYS", "90"))

# ===================================================================
# 6. AGENT EXECUTION
# ===================================================================
# ORCHESTRATOR_CONTRACT §8.4 / §8.5 — Timeout and retry policy.
AGENT_TIMEOUT_SECONDS: int = int(os.getenv("AGENT_TIMEOUT_SECONDS", "30"))
MAX_AGENT_RETRIES: int = int(os.getenv("MAX_AGENT_RETRIES", "2"))
PIPELINE_TIMEOUT_SECONDS: int = int(os.getenv("PIPELINE_TIMEOUT_SECONDS", "120"))

# ===================================================================
# 7. GUARDRAILS
# ===================================================================
# ORCHESTRATOR_CONTRACT §9.3 — Confidence scores below this threshold
# trigger human_review_required status.  Constitution §3 principle 4.
CONFIDENCE_THRESHOLD: int = int(os.getenv("CONFIDENCE_THRESHOLD", "60"))

# ===================================================================
# 8. ANALYSIS SETTINGS
# ===================================================================
# Default look-ahead window (in days) for compliance and inventory
# analysis when the user request does not specify a value.
ANALYSIS_WINDOW_DAYS: int = int(os.getenv("ANALYSIS_WINDOW_DAYS", "30"))

# Default financial analysis period (in days).
DEFAULT_PERIOD_DAYS: int = int(os.getenv("DEFAULT_PERIOD_DAYS", "30"))

# ===================================================================
# 9. GEMINI API
# ===================================================================
# Used by the Communication Agent for LLM-powered report generation.
# Constitution §6: All secrets loaded from .env via config.py.
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# ===================================================================
# 10. BUSINESS RULES
# ===================================================================
# Permitted business_type values accepted by the Orchestrator.
# ORCHESTRATOR_CONTRACT §3.1 — user request validation.
VALID_BUSINESS_TYPES: list[str] = ["retail", "agriculture", "ecommerce"]

# Permitted communication_type values for the Communication Agent.
# AGENT_CONTRACTS §7 — Communication Agent input validation.
VALID_COMMUNICATION_TYPES: list[str] = ["report", "email", "both"]

# Permitted score_type values stored in risk_scores table.
# DATA_MODELS §7 — RiskScore schema.
VALID_SCORE_TYPES: list[str] = [
    "inventory_risk",
    "finance_risk",
    "supplier_risk",
    "compliance_risk",
    "business_risk",
    "business_health",
    "confidence",
]

# Permitted event_type values for compliance events.
# DATA_MODELS §6 — ComplianceEvent schema.
VALID_COMPLIANCE_EVENT_TYPES: list[str] = [
    "tax",
    "license",
    "insurance",
    "regulatory",
    "contract_renewal",
    "other",
]
