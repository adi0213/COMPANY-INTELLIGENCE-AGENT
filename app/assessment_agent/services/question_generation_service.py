import json
import logging
import uuid
from typing import List, Dict, Any

from app.rag.generator import Generator
from app.assessment_agent.utils.memory_db import get_recent_history, add_to_history
from app.assessment_agent.services.question_uniqueness_service import QuestionUniquenessService
from app.assessment_agent.models.schemas import CodingQuestion, AptitudeQuestion

logger = logging.getLogger(__name__)

class QuestionGenerationService:
    def __init__(self):
        self.generator = Generator()
        self.uniqueness_service = QuestionUniquenessService()

    def generate_coding_questions(self, level: str, count: int) -> List[Dict[str, Any]]:
        system_prompt = (
            "You are an expert technical interviewer and competitive programming coach. "
            "Your task is to generate LeetCode-quality coding questions. "
            "The generated questions must be: Original, Non-trivial, Industry-level, Interview-focused, and Algorithmically sound. "
            "Return ONLY valid JSON format. The response must be a JSON array of objects. "
            "Each object must have exactly these keys: 'title', 'difficulty', 'topic', 'problem_statement', "
            "'constraints' (list of strings), 'example_input', 'example_output', 'explanation', "
            "'expected_time_complexity', 'expected_space_complexity'."
        )
        
        topics_map = {
            "beginner": "Arrays, Strings, HashMaps, Sorting, Searching",
            "learner": "Stack, Queue, Linked List, Trees, Binary Search, Sliding Window",
            "expert": "Graphs, Dynamic Programming, Trie, Greedy, Backtracking, Segment Trees, Union Find"
        }
        
        topics = topics_map.get(level.lower(), "Arrays, Strings")
        
        user_prompt = f"Generate {count + 2} coding questions for {level} level focusing on topics: {topics}. Return ONLY a raw JSON array, without markdown formatting or code blocks."

        try:
            import re
            response = self.generator.generate(system_prompt, user_prompt, json_mode=True)
            
            # Use regex to robustly extract JSON array
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = "[]"
            
            raw_questions = json.loads(json_str)
            
            valid_questions = []
            history = get_recent_history("coding")
            
            for q in raw_questions:
                if len(valid_questions) >= count:
                    break
                    
                # Basic validation
                if "problem_statement" not in q or "title" not in q:
                    continue
                    
                # Uniqueness check
                is_unique = self.uniqueness_service.is_unique(q["problem_statement"], history)
                if is_unique:
                    q["id"] = str(uuid.uuid4())
                    valid_questions.append(q)
                    add_to_history(q["problem_statement"], "coding")
            
            return valid_questions
            
        except Exception as e:
            logger.error(f"Error generating coding questions: {e}")
            return []

    def generate_aptitude_questions(self, level: str, count: int) -> List[Dict[str, Any]]:
        system_prompt = (
            "You are an expert aptitude test creator. Generate unique multiple-choice aptitude questions. "
            "Categories include Quantitative (Percentages, Profit & Loss, Probability, Time & Work, Speed Distance Time), "
            "Logical (Pattern Recognition, Seating Arrangement, Coding-Decoding, Blood Relations), "
            "and Verbal (Grammar, Reading Comprehension, Vocabulary). "
            "Return ONLY valid JSON format. The response must be a JSON array of objects. "
            "Each object must have exactly these keys: 'question', 'options' (list of exactly 4 strings), "
            "'correct_answer' (must match one of the options exactly), 'explanation', 'topic', 'difficulty'."
        )
        
        user_prompt = f"Generate {count + 2} aptitude questions for {level} difficulty level across different categories. Return ONLY a raw JSON array, without markdown formatting or code blocks."

        try:
            import re
            response = self.generator.generate(system_prompt, user_prompt, json_mode=True)
            
            # Use regex to robustly extract JSON array
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = "[]"
                
            raw_questions = json.loads(json_str)
            
            valid_questions = []
            history = get_recent_history("aptitude")
            
            for q in raw_questions:
                if len(valid_questions) >= count:
                    break
                    
                # Basic validation
                if "question" not in q or "options" not in q or len(q["options"]) != 4:
                    continue
                    
                # Uniqueness check
                is_unique = self.uniqueness_service.is_unique(q["question"], history)
                if is_unique:
                    q["id"] = str(uuid.uuid4())
                    valid_questions.append(q)
                    add_to_history(q["question"], "aptitude")
                    
            return valid_questions
            
        except Exception as e:
            logger.error(f"Error generating aptitude questions: {e}")
            return []
