"""
Company Cleaner Module

Why we need this:
- In databases and embedding spaces, "Google", "Google LLC", and "Alphabet Google" 
  are three different strings. If we don't normalize them, retrieving all news about 
  "Google" will miss the "Google LLC" articles.
- Normalization (Entity Resolution) is a classic NLP problem.

Architecture & Design Decisions:
- We use a defined list of common legal suffixes (LLC, Inc, Corp, Ltd).
- We use regex with word boundaries `\b` to ensure we don't accidentally strip 
  the letters "inc" from the word "Princess" (though unlikely for a company name, 
  defensive programming is key).

Future Scalability:
- For a true production system, you would integrate a fuzzy matching library 
  (like `thefuzz` or `rapidfuzz`) to match scraped names against a canonical 
  database of known company names.
"""

import re
import logging

logger = logging.getLogger(__name__)

# List of common corporate suffixes to remove
LEGAL_SUFFIXES = [
    r'\bllc\b', r'\binc\.?\b', r'\bcorp\.?\b', r'\bcorporation\b', 
    r'\bltd\.?\b', r'\blimited\b', r'\bcompany\b', r'\bco\.?\b'
]

# Compile the regex pattern once for performance.
# re.IGNORECASE makes it match "LLC", "llc", "Llc".
SUFFIX_PATTERN = re.compile('|'.join(LEGAL_SUFFIXES), re.IGNORECASE)

def normalize_company_name(raw_name: str) -> str:
    """
    Standardizes a company name by removing legal suffixes and excess whitespace.
    
    Internal Workflow:
    1. Check for empty string.
    2. Apply regex to remove suffixes like "Inc.", "LLC".
    3. Remove trailing commas or hyphens left behind.
    4. Strip whitespace and return title cased string (optional, but good for UX).
    """
    if not raw_name or not isinstance(raw_name, str):
        return ""
        
    try:
        # Remove suffixes
        clean_name = SUFFIX_PATTERN.sub('', raw_name)
        
        # Sometimes removing "Inc." leaves a dangling comma, like "Google, "
        clean_name = re.sub(r'[,;\-]\s*$', '', clean_name)
        
        # Clean up double spaces
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        
        # Return Title Case (e.g., "google" -> "Google")
        # Note: Title case isn't perfect for camelCase brands (like "YouTube"), 
        # but it's a good baseline.
        return clean_name.title() if clean_name else raw_name
        
    except Exception as e:
        logger.error(f"Error normalizing company name '{raw_name}': {e}")
        return raw_name.strip()
