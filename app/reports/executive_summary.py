"""
Executive Summary Generator

Why we need this:
- Takes the full combined 10-page draft produced by the agents and condenses it
  into a sharp, 1-page executive summary for busy stakeholders.
"""

import logging
from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class ExecutiveSummaryGenerator:
    def __init__(self):
        self.llm = Generator(model="llama3.1")
        
    def generate(self, full_draft: str) -> str:
        logger.info("Generating Executive Summary...")
        
        system_prompt = (
            "You are a Principal Business Analyst. Your job is to read the provided "
            "Company Intelligence Report and write a highly professional, 2-paragraph "
            "Executive Summary. Do NOT introduce new facts outside of the provided report."
        )
        
        user_prompt = f"Please summarize the following report:\n\n{full_draft}"
        
        return self.llm.generate(system_prompt, user_prompt)
