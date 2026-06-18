import json
import logging
from typing import Dict, Any

from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class AssessmentReportAgent:
    def __init__(self):
        self.generator = Generator()

    def generate_summary(self, overall_score: float, skill_analysis: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the performance.
        """
        system_prompt = (
            "You are an expert technical mentor summarizing an assessment report. "
            "Provide a concise, encouraging, and professional human-readable summary (3-4 sentences max) "
            "highlighting their strengths and pointing out areas for improvement. "
            "Do NOT use markdown bolding or lists, just return plain text."
        )

        user_prompt = (
            f"Overall Score: {overall_score}\n"
            f"Skill Analysis:\n{json.dumps(skill_analysis, indent=2)}\n\n"
            "Generate the summary text."
        )

        try:
            response = self.generator.generate(system_prompt, user_prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating human summary: {e}")
            return "An error occurred while generating your personalized summary. Keep practicing your focus areas to improve!"
