"""
Prompt Builder Module

Why we need this:
- This is where the magic of "Retrieval Grounding" happens.
- We give the LLM both the retrieved context AND explicit instructions to
  supplement with its own world knowledge when the context is sparse.

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
            "You are a Principal AI Architect and Enterprise Intelligence Analyst working for a "
            "world-class Company Intelligence Platform.\n\n"
            "YOUR MANDATE:\n"
            "1. Provide EXHAUSTIVE, highly detailed, precise, and professional answers about the company.\n"
            "2. ALWAYS combine the provided context with your own vast internal world knowledge to create "
            "the most accurate and comprehensive report possible.\n"
            "3. If the provided context is sparse, incomplete, or irrelevant — you MUST use your own "
            "knowledge to fill in ALL gaps. A sparse context is NOT an excuse for a sparse answer.\n"
            "4. NEVER say 'No data available', 'No formal description available', 'I do not have enough "
            "information', 'not mentioned in the context', or any similar phrase. This is STRICTLY FORBIDDEN.\n"
            "5. Format your output professionally with Markdown: use headers (###), bullet points, bold text, "
            "and clear sections. Make it look like a premium consulting report.\n"
            "6. Be specific: include real names, real numbers, real dates, real product names, real technologies. "
            "Generic filler text is UNACCEPTABLE.\n"
            "7. Write at least 200-400 words per section for comprehensive coverage.\n"
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
            f"INSTRUCTIONS: Provide an exhaustive, highly detailed response. Merge the context above "
            f"with your expert world knowledge. If the context is missing key details, supplement them "
            f"from your own knowledge. The user is paying for a premium intelligence report — deliver "
            f"exceptional quality with specific facts, figures, and insights."
        )
        return prompt
