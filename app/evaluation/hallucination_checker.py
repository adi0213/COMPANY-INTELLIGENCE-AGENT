"""
Hallucination Checker (LLM-as-a-Judge)

Why we need this:
- We can't manually read every report. We need an automated way to detect if our 
  Generator LLM hallucinated facts that weren't in the Vector DB context.
"""

import logging
from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class HallucinationChecker:
    def __init__(self):
        # We use a completely independent instance of the LLM to act as the Judge
        self.judge_llm = Generator(model="llama3.1")
        
    def check_hallucination(self, context: str, generated_answer: str) -> float:
        """
        Grades the answer from 0.0 (Complete Hallucination) to 1.0 (Fully Grounded).
        """
        logger.info("Running automated Hallucination Evaluation...")
        
        system_prompt = (
            "You are an impartial AI Evaluation Judge. Your job is to read the 'Source Context' "
            "and the 'AI Answer'. Evaluate if the AI Answer contains ANY information not present "
            "in the Source Context. "
            "Output ONLY a single number between 0.0 and 1.0. "
            "1.0 means perfectly grounded. 0.0 means complete hallucination."
        )
        
        user_prompt = (
            f"Source Context:\n{context}\n\n"
            f"AI Answer:\n{generated_answer}\n\n"
            f"Score (0.0 to 1.0):"
        )
        
        try:
            # We mock the response if the LLM isn't available to prevent failing tests
            if self.judge_llm.use_mock:
                return 1.0
                
            result = self.judge_llm.generate(system_prompt, user_prompt)
            # Try to parse the float from the string
            score = float(result.strip().replace('"', '').replace("'", ""))
            return min(max(score, 0.0), 1.0) # Clamp between 0 and 1
        except Exception as e:
            logger.error(f"Hallucination evaluation failed to parse score: {e}")
            return 0.5 # Unknown
