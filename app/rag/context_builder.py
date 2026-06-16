"""
Context Builder Module

Why we need this:
- The LLM accepts a single string as its prompt. 
- We have a list of Dictionary objects representing our Top-K chunks.
- The Context Builder transforms those Python dictionaries into a highly readable, 
  structured string that the LLM can easily parse.

Token Budgeting:
- If our context limit is strictly tight, we would count tokens here (using `tiktoken`) 
  and truncate chunks that push us over the limit.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ContextBuilder:
    def build_context(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Combines retrieved chunks into a single string.
        """
        if not chunks:
            return "No relevant context found."
            
        logger.info(f"Building context from {len(chunks)} chunks.")
        
        context_parts = []
        for i, chunk in enumerate(chunks):
            # We add clear delimiters so the LLM knows where one document ends and the next begins
            source = chunk.get("metadata", {}).get("source", "Unknown")
            text = chunk.get("text", "")
            
            formatted_chunk = f"--- Document {i+1} (Source: {source}) ---\n{text}\n"
            context_parts.append(formatted_chunk)
            
        final_context = "\n".join(context_parts)
        return final_context
