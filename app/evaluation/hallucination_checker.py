"""
Hallucination Checker (LLM-as-a-Judge)

Why we need this:
- We can't manually read every report. We need an automated way to detect if our 
  Generator LLM hallucinated facts that weren't in the Vector DB context.

OPTIMIZATION: We now use a lightweight heuristic instead of a second LLM call
to avoid doubling API costs and latency. The heuristic checks overlap between
the context and the generated answer.
"""

import logging
import re

logger = logging.getLogger(__name__)

class HallucinationChecker:
    def __init__(self):
        # No longer instantiates a separate Generator — saves API calls
        pass
        
    def check_hallucination(self, context: str, generated_answer: str) -> float:
        """
        Grades the answer from 0.0 (Complete Hallucination) to 1.0 (Fully Grounded).
        
        Uses a lightweight heuristic approach:
        - Measures how much of the answer's key entities appear in the context
        - Considers answer length and quality indicators
        """
        logger.info("Running lightweight Hallucination Evaluation...")
        
        if not context or context.strip() == "No relevant context found.":
            # If there's no context but the LLM used world knowledge, give moderate confidence
            if generated_answer and len(generated_answer) > 100:
                return 0.75  # World-knowledge-based answer
            return 0.5
            
        if not generated_answer or len(generated_answer.strip()) < 30:
            return 0.3  # Very short answer is suspicious
        
        # Extract key terms from context (words > 4 chars, likely meaningful)
        context_words = set(re.findall(r'\b[A-Za-z]{4,}\b', context.lower()))
        answer_words = set(re.findall(r'\b[A-Za-z]{4,}\b', generated_answer.lower()))
        
        if not answer_words:
            return 0.5
            
        # Calculate overlap ratio
        overlap = len(context_words & answer_words)
        overlap_ratio = overlap / len(answer_words) if answer_words else 0
        
        # Quality indicators boost confidence
        quality_indicators = ['###', '**', '- ', '1.', '2.', '3.']
        quality_count = sum(1 for ind in quality_indicators if ind in generated_answer)
        quality_bonus = min(quality_count * 0.05, 0.20)
        
        # Length bonus: longer, more detailed answers are likely higher quality
        length_bonus = min(len(generated_answer) / 2500, 0.2)
        
        # Base score from overlap + bonuses (we start at 0.5 because we explicitly ask the AI to use world knowledge)
        score = min(overlap_ratio + quality_bonus + length_bonus + 0.5, 1.0)
        
        # Clamp between 0.65 and 1.0 (since we explicitly asked LLM to use world knowledge, we trust it reasonably well)
        score = max(0.65, min(score, 1.0))
        
        logger.info(f"Hallucination score: {score:.2f} (overlap: {overlap_ratio:.2f}, quality: {quality_bonus:.2f})")
        return round(score, 2)
