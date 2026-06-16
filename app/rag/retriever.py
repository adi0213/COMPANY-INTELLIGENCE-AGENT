"""
Retriever Module

Why we need this:
- The Vector DB (Chroma) just holds data. The Retriever acts as the bridge between 
  the User's text query and the Vector DB.
- It is responsible for calling the Embedder (Phase 4) on the user's query, and then 
  calling the Search function (Phase 5).

Concepts:
- "Recall": Did we fetch the right document at all? High recall means we fetched it, 
  even if it was buried at position #15 out of 20.
- "Precision": Are the documents we fetched actually relevant? High precision means 
  the top 5 results are EXACTLY what we need.
- Vector Search alone optimizes for RECALL. We fetch Top-K (e.g., K=20) to cast a wide net.
"""

import logging
from typing import List, Dict, Any
from app.vector_db.search import semantic_search

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self, top_k: int = 20):
        """
        Initializes the retriever.
        Notice we fetch K=20, which is a wide net. We will use a Reranker later to narrow it down to K=5.
        """
        self.top_k = top_k
        
    def retrieve(self, query: str, filter_metadata: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Embeds the query and fetches the top K closest chunks.
        """
        logger.info(f"Retrieving top {self.top_k} chunks for query: '{query}'")
        
        # We reuse the semantic_search function from Phase 5
        results = semantic_search(query=query, n_results=self.top_k, filter_metadata=filter_metadata)
        
        logger.info(f"Retrieved {len(results)} chunks.")
        return results
