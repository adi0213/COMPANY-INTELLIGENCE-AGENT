"""
Text Cleaner Module

Why we need this:
- Raw web text is notoriously messy. It contains HTML tags (`<p>`, `<a>`), excessive whitespace, 
  and unwanted symbols (like tracking parameters or emojis in serious news).
- LLMs charge per token. Sending HTML tags wastes context window and money. It also degrades 
  embedding quality (e.g., "Google" and "<h1>Google</h1>" map to different vectors if not cleaned).

Architecture & Design Decisions:
- We use Regular Expressions (`re`) combined with BeautifulSoup for robust HTML stripping.
- We do this defensively: catching errors and ensuring we don't accidentally return empty strings 
  when cleaning fails.

Industry Alternatives:
- For high-volume production, some teams use Rust-based string parsing libraries for extreme speed,
  but Python's `re` and `bs4` are standard and perfectly fine for most architectures.

Future Scalability:
- We can add functions here for specifically removing Markdown, handling different encodings 
  (UTF-8 normalization), and custom regex for PII (Personally Identifiable Information) masking.
"""

import re
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def clean_html_and_whitespace(raw_text: str) -> str:
    """
    Removes HTML tags and normalizes whitespace in a given string.
    
    Internal Workflow:
    1. Check if the input is valid.
    2. Use BeautifulSoup to strip HTML tags safely.
    3. Use Regex to replace multiple spaces/newlines with a single space.
    4. Strip leading/trailing whitespace.
    """
    if not isinstance(raw_text, str) or not raw_text.strip():
        return ""
        
    try:
        # Step 1: Remove HTML tags
        # BeautifulSoup is better than simple Regex `<.*?>` because it handles 
        # malformed HTML (like missing closing tags) gracefully.
        soup = BeautifulSoup(raw_text, "html.parser")
        text_no_html = soup.get_text(separator=" ")
        
        # Step 2: Normalize whitespace
        # \s+ matches any whitespace character (space, tab, newline) one or more times.
        clean_text = re.sub(r'\s+', ' ', text_no_html)
        
        return clean_text.strip()
    except Exception as e:
        logger.warning(f"Error cleaning text '{raw_text[:20]}...': {e}")
        # Fallback to returning original string without HTML if soup fails
        return re.sub(r'\s+', ' ', re.sub(r'<.*?>', ' ', raw_text)).strip()

def remove_special_characters(raw_text: str, keep_punctuation: bool = True) -> str:
    """
    Removes emojis and weird unicode artifacts.
    """
    if not raw_text:
        return ""
        
    if keep_punctuation:
        # Keep alphanumeric and basic punctuation
        # [^\w\s.,!?'"-] means "match anything that is NOT a word char, space, or basic punctuation"
        pattern = r'[^\w\s.,!?\'"\-]'
    else:
        # Keep only alphanumeric and space
        pattern = r'[^\w\s]'
        
    cleaned = re.sub(pattern, '', raw_text)
    return re.sub(r'\s+', ' ', cleaned).strip()
