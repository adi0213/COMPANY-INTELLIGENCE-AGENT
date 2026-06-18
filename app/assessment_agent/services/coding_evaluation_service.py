import json
import logging
from typing import Dict, Any

from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class CodingEvaluationService:
    def __init__(self):
        self.generator = Generator()

    def evaluate_solution(self, question: Dict[str, Any], user_solution: str) -> Dict[str, int]:
        """
        Evaluate a user's coding solution using the LLM.
        """
        # Strip language tag to check if actually empty
        clean_solution = user_solution
        if user_solution and user_solution.startswith("[LANGUAGE:"):
            parts = user_solution.split("]\n", 1)
            if len(parts) > 1:
                clean_solution = parts[1]
            else:
                clean_solution = ""
                
        if not clean_solution or not clean_solution.strip():
            return {
                "correctness": 0,
                "logic": 0,
                "efficiency": 0,
                "readability": 0,
                "edge_cases": 0,
                "overall_score": 0
            }

        system_prompt = (
            "You are an expert technical interviewer evaluating a candidate's code submission. "
            "You will be given the problem statement and the candidate's code. "
            "Evaluate the code on a scale of 0 to 100 for each of the following criteria: "
            "1. correctness (Does it solve the problem?)\n"
            "2. logic (Is the underlying logic sound?)\n"
            "3. efficiency (Time and space complexity compared to optimal)\n"
            "4. readability (Code style, variable names, etc.)\n"
            "5. edge_cases (Does it handle edge cases properly?)\n"
            "Calculate an overall_score (average of the 5 criteria). "
            "Return ONLY valid JSON format. The response must be a JSON object containing exactly these keys: "
            "'correctness', 'logic', 'efficiency', 'readability', 'edge_cases', 'overall_score', all with integer values."
        )

        user_prompt = (
            f"Problem Statement:\n{question.get('problem_statement', 'N/A')}\n\n"
            f"Expected Time Complexity: {question.get('expected_time_complexity', 'N/A')}\n"
            f"Expected Space Complexity: {question.get('expected_space_complexity', 'N/A')}\n\n"
            f"Candidate Code:\n{user_solution}\n\n"
            "Return the JSON evaluation."
        )

        try:
            import re
            response = self.generator.generate(system_prompt, user_prompt, json_mode=True)
            
            # Use regex to robustly extract JSON object
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = "{}"

            eval_scores = json.loads(json_str)
            
            # Validation
            required_keys = ['correctness', 'logic', 'efficiency', 'readability', 'edge_cases', 'overall_score']
            for key in required_keys:
                if key not in eval_scores:
                    eval_scores[key] = 0
                else:
                    try:
                        eval_scores[key] = int(eval_scores[key])
                    except ValueError:
                        eval_scores[key] = 0

            return eval_scores
        except Exception as e:
            logger.error(f"Error evaluating coding solution: {e}")
            return {
                "correctness": 0,
                "logic": 0,
                "efficiency": 0,
                "readability": 0,
                "edge_cases": 0,
                "overall_score": 0
            }
