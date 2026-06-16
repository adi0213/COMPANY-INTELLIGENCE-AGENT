"""
Risk Analysis Generator

Why we need this:
- Executives need to know the threats.
- This LLM prompt specifically hunts for weaknesses, controversies, tech debt,
  hiring freezes, and negative PR in the combined draft.
"""

import logging
from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class RiskAnalysisGenerator:
    def __init__(self):
        self.llm = Generator(model="llama3.1")
        
    def generate(self, full_draft: str) -> str:
        logger.info("Generating Risk Analysis...")
        
        system_prompt = (
            "You are a Risk Management Consultant. Read the provided Company Report "
            "and extract 3 key bullet points highlighting potential risks, weaknesses, "
            "controversies, or challenges facing the company."
        )
        
        user_prompt = f"Extract the risks from this report:\n\n{full_draft}"
        
        return self.llm.generate(system_prompt, user_prompt)
