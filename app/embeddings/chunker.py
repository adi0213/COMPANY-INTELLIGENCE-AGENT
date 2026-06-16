"""
Text Chunker Module

Why we need this:
- LLMs and Embedding models have a maximum "Context Window" (e.g., all-MiniLM-L6-v2 only 
  accepts up to 256 tokens at a time).
- If we pass a 10-page document into the model, it will silently truncate (cut off) everything 
  after 256 tokens.
- We must manually chop long documents into smaller "chunks".

Architecture & Design Decisions:
- We use a "Sliding Window" approach with an overlap. 
- Why overlap? Imagine the sentence: "The CEO of Google is Sundar Pichai."
  If we chunk exactly at the word "is", we get:
    Chunk 1: "The CEO of Google is"
    Chunk 2: "Sundar Pichai."
  Neither chunk makes sense alone. Overlapping ensures context is preserved across boundaries.

Production Best Practices:
- In advanced systems (like LlamaIndex or LangChain), you chunk by semantic boundaries 
  (e.g., splitting by paragraphs `\n\n`, then sentences `. `, then words) rather than 
  blindly cutting at character limits. For this module, we will implement a basic 
  character-based sliding window.
"""

import logging
from typing import List

logger = logging.getLogger(__name__)

class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Initializes the chunker.
        Note: We use character counts here for simplicity. 
        1000 characters is roughly 250 tokens (since 1 token ≈ 4 characters in English).
        
        Args:
            chunk_size (int): Max characters per chunk.
            chunk_overlap (int): Number of characters to overlap between chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """
        Splits a single large string into overlapping chunks.
        """
        if not text or not isinstance(text, str):
            return []
            
        chunks = []
        start = 0
        text_length = len(text)
        
        # Sliding window approach
        while start < text_length:
            end = start + self.chunk_size
            
            # If this isn't the last chunk, try to find a natural break (like a space or period)
            # so we don't cut a word in half.
            if end < text_length:
                # Look backwards from the 'end' to find a space
                # We'll look back at most 50 characters
                last_space = text.rfind(' ', start, end)
                if last_space != -1 and (end - last_space) < 50:
                    end = last_space
                    
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
                
            # Move the window forward, subtracting the overlap
            start = end - self.chunk_overlap
            
            # Prevent infinite loops if overlap is somehow larger than the text progress
            if start <= start - (end - start):
                start += self.chunk_overlap # Force it forward
                
        return chunks
