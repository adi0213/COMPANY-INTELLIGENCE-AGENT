"""
Educational Similarity Module

Why we need this:
- Vector databases like ChromaDB do similarity calculations automatically in C++ for extreme speed.
- However, as a learner, you MUST understand how it works under the hood. 
  "Magic is just math we haven't learned yet."

What is Cosine Similarity?
- It measures the cosine of the angle between two vectors in a multi-dimensional space.
- Formula: dot_product(A, B) / (magnitude(A) * magnitude(B))
- Result is between -1.0 and 1.0. 
  1.0 = Perfect match (vectors point the exact same way)
  0.0 = Orthogonal (no relation)
  -1.0 = Exact opposites

Why not Euclidean Distance?
- Euclidean distance measures the straight line between the ends of two vectors. 
- If you have a short sentence "AI is good" and a massive book about how "AI is good", 
  their magnitudes (lengths) are totally different, so Euclidean distance says they are far apart.
- Cosine Similarity ignores length and only checks the *direction*. Both the sentence and the book 
  point in the "AI is good" direction, so Cosine correctly says they are highly similar!
"""

import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)

def calculate_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Manually calculates the Cosine Similarity between two vectors.
    This is for educational purposes. In production, ChromaDB handles this.
    """
    if not vec_a or not vec_b:
        return 0.0
        
    if len(vec_a) != len(vec_b):
        logger.error("Vectors must have the same number of dimensions to calculate similarity!")
        return 0.0
        
    # Convert to numpy arrays for fast math
    a = np.array(vec_a)
    b = np.array(vec_b)
    
    # 1. Calculate Dot Product (multiply matching indices and sum them up)
    dot_product = np.dot(a, b)
    
    # 2. Calculate Magnitude (length) of each vector using L2 norm
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    # Prevent division by zero
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
        
    # 3. Calculate Cosine
    similarity = dot_product / (norm_a * norm_b)
    
    return float(similarity)
