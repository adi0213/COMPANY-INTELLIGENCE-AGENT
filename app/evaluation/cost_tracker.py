"""
Cost Tracker Module
"""

import logging

logger = logging.getLogger(__name__)

# Very rough estimates
COST_PER_1K_TOKENS = 0.002

def estimate_cost(prompt: str, answer: str) -> float:
    # A rough heuristic: 1 token ~= 4 characters in English
    tokens = (len(prompt) + len(answer)) / 4.0
    cost = (tokens / 1000.0) * COST_PER_1K_TOKENS
    return cost

def count_tokens(text: str) -> int:
    return int(len(text) / 4.0)
