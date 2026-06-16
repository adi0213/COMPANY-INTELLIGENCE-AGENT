"""
Retrieval Metrics

Standard metrics for Vector DB performance.
"""

def calculate_precision_at_k(retrieved_ids: list, relevant_ids: list, k: int) -> float:
    retrieved_k = retrieved_ids[:k]
    relevant_retrieved = set(retrieved_k).intersection(set(relevant_ids))
    return len(relevant_retrieved) / k if k > 0 else 0.0

def calculate_recall_at_k(retrieved_ids: list, relevant_ids: list, k: int) -> float:
    retrieved_k = retrieved_ids[:k]
    relevant_retrieved = set(retrieved_k).intersection(set(relevant_ids))
    return len(relevant_retrieved) / len(relevant_ids) if len(relevant_ids) > 0 else 0.0
