"""
Date Cleaner Module

Why we need this:
- Dates come in thousands of formats: "15/06/2026", "June 15th", "2 days ago", "Yesterday".
- If we want our Vector Database to support chronological filtering (e.g., "Only retrieve news 
  from 2026"), we MUST convert all dates to a standard machine-readable format: ISO-8601 (`YYYY-MM-DD`).

Architecture & Design Decisions:
- Writing custom regex for every date format is impossible. 
- We use the `dateparser` library. It acts as an AI-like heuristics engine that can understand 
  relative times ("2 days ago") and multiple languages.

Industry Best Practices:
- Always use UTC time under the hood. If a date is just a day without timezone, assume UTC 
  or the system's default timezone consistently.
"""

import logging
import dateparser
from datetime import datetime

logger = logging.getLogger(__name__)

def normalize_date(raw_date: str) -> str:
    """
    Parses any human-readable date string and converts it to YYYY-MM-DD.
    
    Internal Workflow:
    1. Check for empty inputs.
    2. Pass the string to dateparser.
    3. If parsed successfully, format as YYYY-MM-DD.
    4. If parsing fails, return a default or the original string (we'll return original to avoid data loss, 
       but log a warning).
    """
    if not raw_date or not isinstance(raw_date, str):
        return ""
        
    try:
        # dateparser is powerful. It handles "yesterday", "2 weeks ago", etc.
        # We set settings to prefer day-first if ambiguous (like 10/11/2026 -> Nov 10th).
        parsed_date = dateparser.parse(raw_date, settings={'PREFER_DAY_OF_MONTH': 'first'})
        
        if parsed_date:
            return parsed_date.strftime("%Y-%m-%d")
        else:
            logger.warning(f"Could not parse date: '{raw_date}'")
            return raw_date.strip()
            
    except Exception as e:
        logger.error(f"Error parsing date '{raw_date}': {e}")
        return raw_date.strip()
