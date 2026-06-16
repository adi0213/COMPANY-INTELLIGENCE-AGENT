"""
Cleaning Service Module

Why we need this:
- We have many small, highly-specialized cleaner functions. 
- This service acts as the Orchestrator for Phase 3. It takes the raw JSON payload, 
  passes specific parts of it through the appropriate cleaners, and constructs 
  a new, normalized payload.

Architecture & Design Decisions:
- We create a new dictionary `clean_payload` rather than modifying `raw_data` in place. 
  Immutability prevents hard-to-track bugs where data is accidentally overwritten.
- We run the cleaners sequentially here since cleaning text/JSON is CPU-bound and very fast,
  unlike network requests which are I/O-bound and required `asyncio.gather` in Phase 2.
"""

import logging
from typing import Dict, Any

from app.cleaners.text_cleaner import clean_html_and_whitespace
from app.cleaners.company_cleaner import normalize_company_name
from app.cleaners.news_cleaner import clean_news_article
from app.cleaners.date_cleaner import normalize_date
from app.cleaners.salary_cleaner import normalize_salary
from app.cleaners.deduplicator import deduplicate_news

from app.utils.storage import save_cleaned_data

logger = logging.getLogger(__name__)

def clean_company_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    The main pipeline for transforming raw data into AI-ready data.
    """
    clean_payload = {}
    company_name = raw_data.get("company", {}).get("name", "Unknown")
    normalized_name = normalize_company_name(company_name)
    
    logger.info(f"Starting data cleaning for {normalized_name}")
    
    # 1. Clean Company Section
    raw_company = raw_data.get("company", {})
    clean_payload["company"] = {
        "name": normalized_name,
        "industry": clean_html_and_whitespace(raw_company.get("industry", "")),
        "headquarters": clean_html_and_whitespace(raw_company.get("headquarters", "")),
        "description": clean_html_and_whitespace(raw_company.get("description", "")),
        "website": raw_company.get("website", ""),
        "employees": raw_company.get("employees", ""),
        "founded": raw_company.get("founded", "")
    }
    
    # 2. Clean News Section
    raw_news = raw_data.get("news", [])
    cleaned_news_list = []
    
    for article in raw_news:
        # Preprocess HTML and check for spam
        clean_article = clean_news_article(article)
        
        # Skip if spam
        if clean_article.get("is_spam"):
            continue
            
        # Normalize date
        clean_article["date"] = normalize_date(clean_article.get("date", ""))
        
        # Remove the 'is_spam' flag before final output to keep it clean
        clean_article.pop("is_spam", None)
        cleaned_news_list.append(clean_article)
        
    # 3. Remove duplicate news (Deduplication)
    clean_payload["news"] = deduplicate_news(cleaned_news_list)
    
    # 4. Clean Jobs Section
    raw_jobs = raw_data.get("jobs", {})
    clean_payload["jobs"] = {
        "open_roles": [clean_html_and_whitespace(role) for role in raw_jobs.get("open_roles", [])],
        "top_hiring_categories": [clean_html_and_whitespace(cat) for cat in raw_jobs.get("top_hiring_categories", [])]
    }
    
    # 5. Clean Salary Section
    raw_salary = raw_data.get("salary", {})
    clean_payload["salary"] = {}
    for role, salary_str in raw_salary.items():
        # Standardize the role key to lowercase with underscores
        clean_role_key = role.lower().replace(" ", "_")
        clean_payload["salary"][clean_role_key] = normalize_salary(salary_str)
        
    # 6. Clean Products Section
    raw_products = raw_data.get("products", {})
    clean_payload["products"] = {
        "products": [clean_html_and_whitespace(p) for p in raw_products.get("products", [])],
        "services": [clean_html_and_whitespace(s) for s in raw_products.get("services", [])]
    }
    
    # Save the cleaned payload
    try:
        # We pass the original company name to the storage to keep the filename consistent
        # though passing normalized_name is also a valid choice.
        save_cleaned_data(company_name, clean_payload)
    except Exception as e:
        logger.error(f"Failed to save cleaned data: {e}")
        
    logger.info(f"Successfully completed data cleaning for {normalized_name}")
    
    return clean_payload
