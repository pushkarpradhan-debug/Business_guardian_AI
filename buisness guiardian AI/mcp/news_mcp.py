# MCP STUB — returns mock data for development/testing. Replace with real API calls in production.
"""News MCP Client Stub."""

from __future__ import annotations
from datetime import datetime, timezone, timedelta
import hashlib
import re
from typing import Any

def fetch_news_data(inputs: dict[str, Any]) -> dict[str, Any]:
    """Validate query terms and retrieve news articles related to suppliers and industry.
    
    Conforms to v1.1 API_CONTRACTS response envelope.
    """
    supplier_names = inputs.get("supplier_names")
    industry_keywords = inputs.get("industry_keywords")
    max_articles = inputs.get("max_articles_per_topic", 5)
    max_age_days = inputs.get("max_age_days", 30)
    
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    try:
        # 1. Validation: At least one of supplier_names or industry_keywords must be non-empty
        if not supplier_names and not industry_keywords:
            return {
                "mcp": "news_mcp",
                "status": "error",
                "error_code": "MISSING_SEARCH_TERMS",
                "error_message": "Either supplier_names or industry_keywords must be provided.",
                "fetched_at": fetched_at
            }
            
        if supplier_names is not None and not isinstance(supplier_names, list):
            return {
                "mcp": "news_mcp",
                "status": "error",
                "error_code": "MISSING_SEARCH_TERMS",
                "error_message": "supplier_names must be a list of strings.",
                "fetched_at": fetched_at
            }
            
        if industry_keywords is not None and not isinstance(industry_keywords, list):
            return {
                "mcp": "news_mcp",
                "status": "error",
                "error_code": "MISSING_SEARCH_TERMS",
                "error_message": "industry_keywords must be a list of strings.",
                "fetched_at": fetched_at
            }
            
        # 2. Validation: max_articles_per_topic range checks
        try:
            max_articles = int(max_articles)
            if not (1 <= max_articles <= 25):
                raise ValueError()
        except (ValueError, TypeError):
            return {
                "mcp": "news_mcp",
                "status": "error",
                "error_code": "INVALID_MAX_ARTICLES",
                "error_message": "max_articles_per_topic must be an integer between 1 and 25.",
                "fetched_at": fetched_at
            }
            
        # 3. Validation: max_age_days range checks
        try:
            max_age_days = int(max_age_days)
            if not (1 <= max_age_days <= 90):
                raise ValueError()
        except (ValueError, TypeError):
            return {
                "mcp": "news_mcp",
                "status": "error",
                "error_code": "INVALID_MAX_AGE",
                "error_message": "max_age_days must be an integer between 1 and 90.",
                "fetched_at": fetched_at
            }
            
        # Mock articles databases
        all_supplier_news = []
        if supplier_names:
            for s_name in supplier_names:
                if not isinstance(s_name, str) or not s_name:
                    continue
                if "Alpha" in s_name:
                    all_supplier_news.append({
                        "article_id": hashlib.md5(f"alpha_news_{fetched_at}_{s_name}".encode()).hexdigest(),
                        "supplier_name": s_name,
                        "headline": "Alpha Supplies Faces Short-Term Supply Chain Disruptions",
                        "summary": "Alpha Supplies announced minor logistical bottlenecks at their main packaging warehouse, causing potential shipment delays.",
                        "source": "Supply Chain Logistics Journal",
                        "published_date": "2026-06-24",
                        "sentiment": "negative",
                        "url": "https://sclj.example.com/alpha-disruptions"
                    })
                elif "Beta" in s_name:
                    all_supplier_news.append({
                        "article_id": hashlib.md5(f"beta_news_{fetched_at}_{s_name}".encode()).hexdigest(),
                        "supplier_name": s_name,
                        "headline": "Beta Logistics Expands Canadian Shipping Fleet",
                        "summary": "Beta Logistics has added 15 green electric delivery vans to its Canadian fleet, promising faster local distribution.",
                        "source": "Green Transports News",
                        "published_date": "2026-06-25",
                        "sentiment": "positive",
                        "url": "https://gtn.example.com/beta-expansion"
                    })
                    
        all_industry_news = []
        if industry_keywords:
            for kw in industry_keywords:
                if not isinstance(kw, str) or not kw:
                    continue
                all_industry_news.append({
                    "article_id": hashlib.md5(f"ind_{kw}_{fetched_at}".encode()).hexdigest(),
                    "keyword": kw,
                    "headline": f"Global Trends in {kw.capitalize()} Market Outlook",
                    "summary": f"Recent industry forecasts point towards robust growth in {kw} technologies, though inflation concerns remain.",
                    "source": "Global Business Insider",
                    "published_date": "2026-06-23",
                    "sentiment": "neutral",
                    "url": f"https://gbi.example.com/trends-{kw}"
                })
                
        # 4. Perform integrity check on news date formats
        date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        for article in all_supplier_news + all_industry_news:
            pub_date = article.get("published_date")
            if not pub_date or not isinstance(pub_date, str) or not date_regex.match(pub_date):
                return {
                    "mcp": "news_mcp",
                    "status": "error",
                    "error_code": "INVALID_DATE_FORMAT",
                    "error_message": "Article published_date violates YYYY-MM-DD format.",
                    "fetched_at": fetched_at
                }
            try:
                datetime.strptime(pub_date, "%Y-%m-%d")
            except ValueError:
                return {
                    "mcp": "news_mcp",
                    "status": "error",
                    "error_code": "INVALID_DATE_FORMAT",
                    "error_message": "Article contains an invalid calendar published_date.",
                    "fetched_at": fetched_at
                }
                
        # 5. Filter by age
        now = datetime.now(timezone.utc)
        current_date_str = now.strftime("%Y-%m-%d")
        min_date_str = (now - timedelta(days=max_age_days)).strftime("%Y-%m-%d")
        
        filtered_supplier_news = [
            art for art in all_supplier_news
            if min_date_str <= art["published_date"] <= current_date_str
        ]
        
        filtered_industry_news = [
            art for art in all_industry_news
            if min_date_str <= art["published_date"] <= current_date_str
        ]
        
        # Apply max_articles cap per topic (i.e. overall list slicing for stub simplicity)
        sliced_supplier_news = filtered_supplier_news[:max_articles]
        sliced_industry_news = filtered_industry_news[:max_articles]
        
        return {
            "mcp": "news_mcp",
            "status": "success",
            "data": {
                "supplier_news": sliced_supplier_news,
                "industry_news": sliced_industry_news,
                "total_supplier_articles": len(sliced_supplier_news),
                "total_industry_articles": len(sliced_industry_news)
            },
            "warnings": None,
            "fetched_at": fetched_at
        }
        
    except Exception as e:
        return {
            "mcp": "news_mcp",
            "status": "error",
            "error_code": "FETCH_FAILED",
            "error_message": f"An unexpected error occurred while fetching news data: {str(e)}",
            "fetched_at": fetched_at
        }
