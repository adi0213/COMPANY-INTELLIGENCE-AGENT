"""
Reranker Module

Why we need this:
- Basic vector search (Bi-Encoders) embeds the Query and the Document completely separately.
  This is extremely fast, but it misses linguistic nuance. 
  "How to kill a process in Linux" and "Linux process killed me" might have similar vectors 
  because they share the same words, but completely different meanings!
- A Reranker (Cross-Encoder) takes BOTH the Query and the Document and passes them into the 
  Transformer neural network AT THE SAME TIME. The network calculates exactly how relevant they 
  are to each other.

Workflow:
1. Retriever fetches Top 20 documents.
2. Reranker scores all 20 against the query.
3. Reranker sorts them and returns the Top 5.

Industry Standard:
- Cohere Rerank API is heavily used in production.
- For local models, `cross-encoder/ms-marco-MiniLM-L-6-v2` via `sentence-transformers` is king.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# To prevent massive memory usage on your constrained machine, we will use a "Mock Reranker" 
# for educational purposes. In a real environment, you would import CrossEncoder here.
# from sentence_transformers.cross_encoder import CrossEncoder

class Reranker:
    def __init__(self, top_k: int = 5):
        """
        Initializes the Reranker.
        """
        self.top_k = top_k
        logger.info("Initializing Mock Reranker (skipping CrossEncoder to save RAM).")
        # In production:
        # self.model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    def rerank(self, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scores and re-sorts the chunks.
        """
        if not chunks:
            return []
            
        logger.info(f"Re-ranking {len(chunks)} chunks...")
        
        # In a real CrossEncoder:
        # pairs = [[query, chunk["text"]] for chunk in chunks]
        # scores = self.model.predict(pairs)
        # for i, score in enumerate(scores):
        #     chunks[i]["relevance_score"] = float(score)
        # chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # MOCK IMPLEMENTATION: We simply return the top K from the original vector search,
        # assuming the vector search was already decent.
        reranked = chunks[:self.top_k]
        
        logger.info(f"Kept top {len(reranked)} chunks after re-ranking.")
        return reranked
