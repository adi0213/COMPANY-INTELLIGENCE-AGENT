"""
Semantic Search Module

Why we need this:
- This is the "Retrieval" in RAG (Retrieval-Augmented Generation).
- When a user asks "Who did Google hire recently?", we must find the exact chunks of text 
  that answer this before we send anything to the LLM.

Architecture & Design Decisions:
- We take the user's string query, embed it using the exact same `Embedder` model, and 
  use that query vector to search the database.
- We return the Top-K results (e.g., the 5 most similar chunks).
- We also allow optional metadata filtering (e.g., only search where `company == "Google"`).

Why not return all results?
- LLMs have finite context windows. We must only pass the most highly relevant data (Top-K) 
  to the LLM, discarding the rest to save money and prevent "Context Dilution" (where the LLM 
  gets confused by too much irrelevant information).
"""

import logging
from typing import List, Dict, Any, Optional

from app.vector_db.chroma_client import get_chroma_client, get_or_create_collection
from app.embeddings.embedder import Embedder

logger = logging.getLogger(__name__)

# Initialize embedder once globally for the search module to avoid reloading it on every query
search_embedder = Embedder()

def semantic_search(query: str, n_results: int = 5, filter_metadata: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """
    Performs a vector similarity search in ChromaDB.
    
    Internal Workflow:
    1. Embed the user's query into a vector.
    2. Query ChromaDB using that vector, requesting `n_results`.
    3. Apply `filter_metadata` via Chroma's `where` clause if provided.
    4. Format and return the results.
    """
    if not query:
        return []
        
    logger.info(f"Performing semantic search for: '{query}'")
    
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    
    # 1. Embed the query
    query_vector = search_embedder.generate_embedding(query)
    
    try:
        # 2 & 3. Query the DB
        # If filter_metadata is provided, it must match the exact key-value pairs stored during indexing.
        db_results = collection.query(
            query_embeddings=[query_vector],
            n_results=n_results,
            where=filter_metadata,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        
        # ChromaDB returns lists of lists because you can pass multiple query vectors at once.
        # We only passed 1, so we look at index [0].
        if db_results and db_results["ids"] and len(db_results["ids"][0]) > 0:
            for i in range(len(db_results["ids"][0])):
                # Distance in Chroma for cosine space is actually (1 - cosine_similarity).
                # Lower distance = more similar.
                result = {
                    "id": db_results["ids"][0][i],
                    "text": db_results["documents"][0][i],
                    "metadata": db_results["metadatas"][0][i],
                    "distance": db_results["distances"][0][i]
                }
                formatted_results.append(result)
                
        return formatted_results
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []
