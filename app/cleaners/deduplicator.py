"""
Deduplicator Engine

Why we need this:
- Duplicates are the enemy of RAG (Retrieval-Augmented Generation).
- If the Vector DB contains 5 identical articles about a product launch, a search query 
  will retrieve those 5 duplicates, leaving no room in the LLM context window for other 
  important context (like financial data or past events). This causes "Context Starvation".

Architecture & Design Decisions:
- We use SHA-256 Hashing. Hashing converts a string (like a news title) into a fixed-length signature.
- We maintain a Python `set` of `seen_hashes`. Lookups in a `set` are O(1) time complexity, 
  making this highly scalable.
- Why not just string comparison (`title1 == title2`)? Hashes are faster to compare and 
  consume less memory when dealing with thousands of long articles.

Future Scalability:
- For "fuzzy" duplicates (articles that are 90% similar but have different titles), 
  you would use MinHash or SimHash instead of exact cryptographic hashes like SHA-256.
"""

import hashlib
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def generate_hash(text: str) -> str:
    """Generates a SHA-256 hash for a given string."""
    if not text:
        return ""
    # We lowercase and strip to ensure minor whitespace differences don't break the hash match
    normalized_text = text.lower().strip()
    return hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()

def deduplicate_news(news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Removes duplicate news articles based on their titles.
    """
    if not news_list:
        return []
        
    seen_hashes = set()
    unique_news = []
    
    for article in news_list:
        title = article.get("title", "")
        
        # If there's no title, we skip deduplication for this item and just add it
        if not title:
            unique_news.append(article)
            continue
            
        article_hash = generate_hash(title)
        
        if article_hash not in seen_hashes:
            seen_hashes.add(article_hash)
            unique_news.append(article)
        else:
            logger.info(f"Dropped duplicate article: '{title[:30]}...'")
            
    return unique_news
