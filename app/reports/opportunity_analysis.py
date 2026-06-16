"""
Opportunity Analysis Generator

Why we need this:
- Looks for "Blue Ocean" strategy elements, growth signals, and new product lines.
"""

import logging
from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class OpportunityAnalysisGenerator:
    def __init__(self):
        self.llm = Generator(model="llama3.1")
        
    def generate(self, full_draft: str) -> str:
        logger.info("Generating Opportunity Analysis...")
        
        system_prompt = (
            "You are a Strategic Growth Consultant. Read the provided Company Report "
            "and extract 3 key bullet points highlighting potential opportunities, "
            "new markets, or strategic advantages the company possesses."
        )
        
        user_prompt = f"Extract the opportunities from this report:\n\n{full_draft}"
        
        return self.llm.generate(system_prompt, user_prompt)
