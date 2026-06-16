"""
Vector Database Indexer

Why we need this:
- We have raw strings, their vector embeddings, and their metadata. We need to save them 
  to ChromaDB so we can search them later.
- This process is called "Indexing".

Architecture & Design Decisions:
- ChromaDB collections take `ids`, `embeddings`, `metadatas`, and `documents` (the raw text).
- By storing the raw text (`documents`) alongside the vectors, our semantic search can 
  return the actual human-readable sentences to the LLM. If we only stored vectors, 
  we wouldn't know what text the vector belonged to!

Batching:
- We index in batches (e.g., 100 chunks at a time) to avoid memory overload and timeout errors 
  when dealing with thousands of vectors.
"""

import logging
from typing import List, Dict, Any

from app.vector_db.chroma_client import get_chroma_client, get_or_create_collection

logger = logging.getLogger(__name__)

def index_chunks(chunks: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], ids: List[str]):
    """
    Inserts or updates chunks in the ChromaDB vector database.
    
    Internal Workflow:
    1. Validate that all lists have the same length.
    2. Get the ChromaDB collection.
    3. Use the `.upsert()` method. Upsert means "Update if it exists, Insert if it's new".
       This is crucial because if we run the pipeline twice on the same data, we don't 
       want duplicate vectors in the database.
    """
    if not chunks:
        logger.info("No chunks to index.")
        return
        
    if not (len(chunks) == len(embeddings) == len(metadatas) == len(ids)):
        raise ValueError("Lengths of chunks, embeddings, metadatas, and ids must be exactly equal.")
        
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    
    logger.info(f"Indexing {len(chunks)} chunks into ChromaDB...")
    
    try:
        # We use upsert to prevent duplicates if the pipeline is rerun
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=chunks
        )
        logger.info("Successfully indexed chunks.")
    except Exception as e:
        logger.error(f"Failed to index chunks: {e}")
        raise
