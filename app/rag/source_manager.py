"""
Source Manager Module

Why we need this:
- Enterprise Trust. Users will not trust an AI that just spits out facts without 
  pointing to exactly where it got them.
- This module extracts the metadata from the final Top-K chunks and packages them 
  as citations.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SourceManager:
    def extract_sources(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Extracts clean citation data from the retrieved chunks.
        """
        logger.info("Extracting sources for attribution.")
        
        sources = []
        for i, chunk in enumerate(chunks):
            meta = chunk.get("metadata", {})
            sources.append({
                "document_number": i + 1,
                "source_type": meta.get("source", "Unknown"),
                "company": meta.get("company", "Unknown"),
                "date": meta.get("date", "N/A"),
                "chunk_id": chunk.get("id", "Unknown")
            })
            
        return sources
