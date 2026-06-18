import re
from typing import List

class QuestionUniquenessService:
    def __init__(self):
        pass

    def _tokenize(self, text: str) -> set:
        """Simple word tokenization and lowercasing."""
        words = re.findall(r'\b\w+\b', text.lower())
        return set(words)

    def _calculate_jaccard_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two strings."""
        set1 = self._tokenize(text1)
        set2 = self._tokenize(text2)
        
        if not set1 and not set2:
            return 1.0
            
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

    def is_unique(self, new_question: str, history: List[str], threshold: float = 0.75) -> bool:
        """
        Check if the new question is unique compared to the history.
        If similarity to any previous question is above the threshold, it's a duplicate.
        """
        for old_question in history:
            similarity = self._calculate_jaccard_similarity(new_question, old_question)
            if similarity > threshold:
                return False
        return True
