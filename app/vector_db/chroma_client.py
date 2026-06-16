"""
ChromaDB Client Manager — Singleton Pattern

Uses a module-level singleton to avoid re-creating the ChromaDB client
and collection on every request, which wastes file handles and memory.
"""

import os
import logging
import chromadb

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DB_DIR = os.path.join(BASE_DIR, "data", "chroma_db")

# Module-level singletons
_client = None
_collection = None


def get_chroma_client():
    """Returns a singleton persistent ChromaDB client."""
    global _client
    if _client is None:
        os.makedirs(CHROMA_DB_DIR, exist_ok=True)
        logger.info(f"Initializing ChromaDB client at {CHROMA_DB_DIR}")
        _client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return _client


def get_or_create_collection(client=None, collection_name: str = "company_intelligence"):
    """Returns a singleton collection handle."""
    global _collection
    if _collection is None:
        if client is None:
            client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(f"ChromaDB collection '{collection_name}' ready.")
    return _collection
