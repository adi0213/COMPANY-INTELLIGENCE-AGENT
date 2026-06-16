"""
Storage Utilities

Why we need this:
- We need a reusable way to save our collected raw data to the filesystem.
- Keeping this separate from the Service layer means if we later switch to AWS S3, 
  MongoDB, or Postgres, we only have to change code here, not in our business logic.

Architecture & Design Decisions:
- We save the output to `data/raw/` with a timestamped filename (e.g., `google_2026_06_15.json`).
- This allows us to track how a company changes over time (Data Versioning), which is critical 
  for building robust ML models.
"""

import json
import os
import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Resolve the absolute path to the data/raw directory, relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

def save_raw_data(company_name: str, payload: Dict[str, Any]) -> str:
    """
    Saves the aggregated payload to a JSON file.
    
    Args:
        company_name (str): The name of the company.
        payload (Dict[str, Any]): The aggregated data dictionary.
        
    Returns:
        str: The path to the saved file.
    """
    # Ensure the directory exists
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    # Generate timestamped filename
    date_str = datetime.now().strftime("%Y_%m_%d")
    # Sanitize company name for filename (e.g., "Google LLC" -> "google_llc")
    safe_name = "".join([c if c.isalnum() else "_" for c in company_name.lower()]).strip("_")
    
    filename = f"{safe_name}_{date_str}.json"
    filepath = os.path.join(RAW_DATA_DIR, filename)
    
    try:
        # Write the JSON payload to disk
        # Best Practice: Use utf-8 encoding to avoid UnicodeEncodeError with special characters.
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Successfully saved raw data for {company_name} to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to save data for {company_name}: {e}")
        raise

CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")

def save_cleaned_data(company_name: str, payload: Dict[str, Any]) -> str:
    """
    Saves the cleaned and normalized payload to a JSON file.
    """
    os.makedirs(CLEANED_DATA_DIR, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y_%m_%d")
    safe_name = "".join([c if c.isalnum() else "_" for c in company_name.lower()]).strip("_")
    
    filename = f"{safe_name}_{date_str}_clean.json"
    filepath = os.path.join(CLEANED_DATA_DIR, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Successfully saved clean data for {company_name} to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to save clean data for {company_name}: {e}")
        raise
