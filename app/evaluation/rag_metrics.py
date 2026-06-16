"""
RAG Metrics

Wraps hallucination checking and faithfulness into a unified interface.
"""

from app.evaluation.hallucination_checker import HallucinationChecker

checker = HallucinationChecker()

def evaluate_rag_output(context: str, generated_answer: str) -> float:
    return checker.check_hallucination(context, generated_answer)
