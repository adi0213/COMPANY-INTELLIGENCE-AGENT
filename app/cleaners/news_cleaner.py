"""
News Cleaner Module

Why we need this:
- News RSS feeds often contain clickbait, sponsored content labels, and tracking URLs.
- Keeping this garbage in the dataset harms the RAG model's ability to pull factual, 
  high-quality context.

Architecture & Design Decisions:
- We import and reuse `clean_html_and_whitespace` from `text_cleaner.py`. This is the DRY 
  (Don't Repeat Yourself) principle.
- We check the title/summary against a blacklist of common clickbait/sponsored phrases. If found,
  we flag it or skip it entirely in the service layer.

Industry Alternatives:
- Advanced setups use small, fast LLMs (like Llama 3 8B or Mistral) or zero-shot classifiers 
  to score news articles for "Information Density" and drop articles that score too low. 
  For Phase 3, keyword filtering is much faster and cheaper.
"""

import logging
from typing import Dict, Any
from app.cleaners.text_cleaner import clean_html_and_whitespace

logger = logging.getLogger(__name__)

# Basic heuristic to detect low-quality news
SPAM_KEYWORDS = ["sponsored", "promoted", "advertisement", "click here", "subscribe now"]

def clean_news_article(article: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cleans a single news article dictionary.
    
    Internal Workflow:
    1. Extract fields.
    2. Strip HTML from title and summary/content using text_cleaner.
    3. Flag as spam if it contains sponsored keywords.
    4. Clean the URL by stripping query parameters (tracking tags).
    """
    if not article:
        return {}
        
    try:
        # 1. Clean HTML from text fields
        title = clean_html_and_whitespace(article.get("title", ""))
        source = clean_html_and_whitespace(article.get("source", ""))
        
        # 2. Check for spam/sponsored content
        # We do this case-insensitively
        title_lower = title.lower()
        is_spam = any(keyword in title_lower for keyword in SPAM_KEYWORDS)
        
        # 3. Clean URL (Remove tracking parameters like ?utm_source=...)
        # e.g., https://news.com/article?utm_source=google -> https://news.com/article
        raw_link = article.get("link", "")
        clean_link = raw_link.split('?')[0] if '?' in raw_link else raw_link
        
        return {
            "title": title,
            "source": source,
            "date": article.get("date", ""), # We will clean this in date_cleaner later
            "link": clean_link,
            "is_spam": is_spam
        }
    except Exception as e:
        logger.error(f"Error cleaning news article: {e}")
        return article # Return raw if cleaning fails
