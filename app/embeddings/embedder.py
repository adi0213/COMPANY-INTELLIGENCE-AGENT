"""
Embedder Module

Generates deterministic pseudo-random embeddings for vector indexing.
Uses a lightweight hash-based approach to avoid loading PyTorch/SentenceTransformers
which would exhaust system memory on resource-constrained machines.
"""

import logging
import math
import hashlib
import struct
from typing import List

logger = logging.getLogger(__name__)


class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the Embedder in lightweight mock mode.
        """
        self.model_name = model_name
        self.dimension = 384
        logger.info("Embedder initialized (lightweight mode, no PyTorch dependency).")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates a deterministic 384-dim embedding vector from text using hashing.
        Produces consistent vectors so the same text always maps to the same point
        in vector space, enabling meaningful cosine similarity search.
        """
        if not text:
            return []

        vector = []
        salt = 0
        # Each SHA-512 hash produces 64 bytes = 16 unsigned 32-bit integers.
        # We need ceil(384 / 16) = 24 hashes to fill 384 floats.
        while len(vector) < self.dimension:
            h = hashlib.sha512(f"{salt}:{text}".encode("utf-8")).digest()
            ints = struct.unpack("16I", h)
            # Normalize to [-1.0, 1.0]: max 32-bit int is 4294967295
            floats = [(v / 2147483647.5) - 1.0 for v in ints]
            vector.extend(floats)
            salt += 1

        # Trim to exact dimension
        vector = vector[: self.dimension]
        return vector

    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of strings.
        """
        if not texts:
            return []
        return [self.generate_embedding(t) for t in texts]
