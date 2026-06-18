from typing import List, Dict, Any

class AptitudeEvaluationService:
    def __init__(self):
        pass

    def evaluate_answers(self, questions: List[Dict[str, Any]], user_answers: List[str]) -> Dict[str, Any]:
        """
        Evaluate multiple-choice aptitude answers.
        """
        correct_count = 0
        incorrect_count = 0
        topic_breakdown = {}

        for i, question in enumerate(questions):
            topic = question.get("topic", "General")
            if topic not in topic_breakdown:
                topic_breakdown[topic] = {"correct": 0, "total": 0}
            
            topic_breakdown[topic]["total"] += 1
            
            user_answer = user_answers[i] if i < len(user_answers) else ""
            correct_answer = question.get("correct_answer", "")
            
            # Simple string matching (can be improved if options format varies slightly)
            if user_answer.strip().lower() == correct_answer.strip().lower():
                correct_count += 1
                topic_breakdown[topic]["correct"] += 1
            else:
                incorrect_count += 1

        total = correct_count + incorrect_count
        percentage = (correct_count / total * 100) if total > 0 else 0.0

        return {
            "correct_count": correct_count,
            "incorrect_count": incorrect_count,
            "percentage": round(percentage, 2),
            "topic_breakdown": topic_breakdown
        }
