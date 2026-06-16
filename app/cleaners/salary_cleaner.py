"""
Salary Cleaner Module

Why we need this:
- Raw salaries look like "$150K", "150,000 USD", "$150k/year", "120k-140k".
- We need structured integers (`min_salary`, `max_salary`) so that our downstream 
  LLM can do math (e.g., "What is the average ML engineer salary?").

Architecture & Design Decisions:
- We use regex to extract all numbers from the string.
- We check for multipliers like 'k' or 'K' and multiply by 1,000.
- We extract the currency based on symbols ('$') or acronyms ('USD').

Common Mistakes:
- Assuming all salaries are yearly. Some are hourly ("$50/hr"). For this MVP Phase 3, 
  we will assume yearly but note that handling pay periods is the next scale step.
"""

import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def normalize_salary(raw_salary: str) -> Dict[str, Any]:
    """
    Parses a salary string into a structured dictionary.
    
    Example: 
        Input: "$150k - 200K"
        Output: {"currency": "USD", "min_salary": 150000, "max_salary": 200000}
    """
    result = {
        "currency": "USD", # Default
        "min_salary": None,
        "max_salary": None
    }
    
    if not raw_salary or not isinstance(raw_salary, str):
        return result
        
    try:
        # 1. Detect Currency
        if '€' in raw_salary or 'EUR' in raw_salary.upper():
            result["currency"] = "EUR"
        elif '£' in raw_salary or 'GBP' in raw_salary.upper():
            result["currency"] = "GBP"
        elif '₹' in raw_salary or 'INR' in raw_salary.upper():
             result["currency"] = "INR"
             
        # 2. Extract Numbers
        # This regex matches numbers with optional decimals and an optional 'k' or 'm'
        # e.g., 150, 150.5, 150k, 1.5m
        matches = re.findall(r'(\d+(?:\.\d+)?)\s*([kmKM])?', raw_salary.replace(',', ''))
        
        parsed_numbers = []
        for match in matches:
            num = float(match[0])
            multiplier = match[1].lower()
            
            if multiplier == 'k':
                num *= 1000
            elif multiplier == 'm':
                num *= 1000000
                
            parsed_numbers.append(int(num))
            
        if not parsed_numbers:
            return result
            
        # 3. Assign Min/Max
        if len(parsed_numbers) == 1:
            result["min_salary"] = parsed_numbers[0]
            result["max_salary"] = parsed_numbers[0]
        else:
            result["min_salary"] = min(parsed_numbers)
            result["max_salary"] = max(parsed_numbers)
            
        return result
        
    except Exception as e:
        logger.error(f"Error parsing salary '{raw_salary}': {e}")
        return result
