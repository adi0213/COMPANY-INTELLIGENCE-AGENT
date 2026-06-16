"""
Tokenizer Educational Module

Why we need this:
- Models don't read "Google". They read arrays of integers.
- Tokenization bridges human text and machine math.

Types of Tokenizers:
- BPE (Byte-Pair Encoding): Used by OpenAI (tiktoken).
- WordPiece: Used by BERT.
- SentencePiece: Used by Llama / T5.

What does it do?
- It maps sub-words to IDs. 
  "Google" -> [1234]
  "develops" -> [456]
  "AI" -> [789]

Why not just split by spaces (Word Tokenization)?
- Because there are infinite words (especially with misspellings or new slang). 
  Sub-word tokenizers ensure the vocabulary size is fixed (e.g., 50,257 tokens) 
  and can construct ANY word from smaller byte-pairs.

Note:
For our actual embeddings (all-MiniLM-L6-v2), `sentence-transformers` handles 
tokenization under the hood using WordPiece. This module uses `tiktoken` purely 
for educational visualization so you can SEE the tokens.
"""

import logging
import tiktoken
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class EducationalTokenizer:
    def __init__(self, model_name: str = "cl100k_base"):
        """
        Initializes the tokenizer. 'cl100k_base' is the encoding used by GPT-4.
        """
        try:
            self.encoding = tiktoken.get_encoding(model_name)
        except Exception as e:
            logger.error(f"Failed to load tokenizer: {e}")
            self.encoding = None

    def visualize_tokens(self, text: str) -> Dict[str, Any]:
        """
        Shows exactly how a string is broken into tokens and IDs.
        """
        if not self.encoding or not text:
            return {"text": text, "tokens": [], "ids": [], "count": 0}
            
        # 1. Encode text to IDs
        token_ids = self.encoding.encode(text)
        
        # 2. Decode each ID back to its string representation so we can see the cuts
        token_strings = [self.encoding.decode([t_id]) for t_id in token_ids]
        
        result = {
            "original_text": text,
            "token_count": len(token_ids),
            "tokens": token_strings,
            "token_ids": token_ids
        }
        
        # Log it for educational purposes
        logger.info(f"Tokenized: '{text}' -> {len(token_ids)} tokens")
        return result
