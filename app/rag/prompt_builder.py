"""
Prompt Builder Module

Why we need this:
- This is where the magic of "Retrieval Grounding" happens.
- If you don't explicitly forbid the LLM from hallucinating, it WILL hallucinate.

Architecture & Design Decisions:
- We split prompts into two parts:
  1. System Prompt: Defines the persona and strict rules.
  2. User Prompt: Contains the dynamic Context and the user's Question.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PromptBuilder:
    def get_system_prompt(self) -> str:
        """
        The absolute rules the LLM must follow.
        """
        return (
            "You are a highly analytical Company Intelligence Assistant. "
            "Your job is to answer questions about a company based STRICTLY on the provided context.\n"
            "RULES:\n"
            "1. If the answer is not contained in the context, say exactly: 'I do not have enough information to answer that.'\n"
            "2. Do NOT use your pre-trained knowledge to answer.\n"
            "3. Be concise, professional, and accurate."
        )
        
    def build_user_prompt(self, question: str, context: str) -> str:
        """
        Injects the context and question into a template.
        """
        logger.info("Building finalized prompt.")
        
        prompt = (
            f"Here is the retrieved context regarding the company:\n\n"
            f"{context}\n\n"
            f"Question: {question}\n\n"
            f"Answer the question based ONLY on the context above."
        )
        return prompt
