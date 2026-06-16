"""
Metadata Engine

Why we need this:
- Vectors only understand semantic meaning, not absolute facts.
- If a user asks: "What were Google's hiring trends in 2024?"
  The vector search will find articles about hiring, but it doesn't know *when* they were published.
- Metadata solves this. We attach dictionaries (key-value pairs) to every vector.

Enterprise RAG Patterns:
- "Pre-filtering": We tell the Vector DB "Only search vectors where `date >= 2024-01-01`". 
  This reduces the search space from 1,000,000 vectors to 10,000 vectors BEFORE doing the 
  heavy cosine similarity math.
- "Post-filtering": Search all vectors, then drop the ones that don't match the metadata. 
  Pre-filtering is much better for performance.

What we do here:
- We create a simple factory function to stamp every chunk with its lineage (where it came from).
"""

import hashlib
import time
from typing import Dict, Any

def create_metadata(company_name: str, source_type: str, date: str = "", extra_tags: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Constructs a metadata dictionary for a vector chunk.
    
    Args:
        company_name (str): The entity this chunk belongs to (e.g., "Google").
        source_type (str): Where it came from (e.g., "news", "jobs", "overview").
        date (str): The ISO-8601 date, if applicable.
        extra_tags (Dict): Any other keys you want to index.
        
    Returns:
        Dict[str, Any]: The finalized metadata payload.
    """
    metadata = {
        "company": company_name,
        "source": source_type,
        "indexed_at": int(time.time()) # Unix timestamp for when it entered the DB
    }
    
    if date:
        metadata["date"] = date
        
    if extra_tags:
        metadata.update(extra_tags)
        
    return metadata

def generate_chunk_id(company_name: str, source_type: str, chunk_index: int, content: str) -> str:
    """
    Generates a deterministic, unique ID for a chunk.
    This prevents us from inserting the exact same chunk into the Vector DB twice.
    """
    unique_string = f"{company_name}_{source_type}_{chunk_index}_{content[:50]}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
