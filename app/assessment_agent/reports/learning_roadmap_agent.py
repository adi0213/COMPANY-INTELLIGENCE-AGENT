import json
import logging
from typing import Dict, Any

from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class LearningRoadmapAgent:
    def __init__(self):
        self.generator = Generator()

    def generate_roadmap(self, skill_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a 4-week learning roadmap based on identified weaknesses.
        Returns a dict matching the ReportRoadmap schema.
        """
        system_prompt = (
            "You are an expert technical mentor. Based on a candidate's skill analysis, "
            "create a personalized 4-week learning roadmap. "
            "Focus primarily on addressing their weaknesses and focus areas. "
            "Return ONLY valid JSON format. The response must be a JSON object containing exactly these keys: "
            "'week_1' (list of strings), 'week_2' (list of strings), 'week_3' (list of strings), 'week_4' (list of strings)."
        )

        user_prompt = f"Skill Analysis:\n{json.dumps(skill_analysis, indent=2)}\n\nGenerate the 4-week roadmap JSON."

        try:
            response = self.generator.generate(system_prompt, user_prompt)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]

            roadmap = json.loads(response.strip())
            
            # Validation
            required_keys = ['week_1', 'week_2', 'week_3', 'week_4']
            for key in required_keys:
                if key not in roadmap:
                    roadmap[key] = ["Practice recommended topics"]
                    
            return roadmap
        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            return {
                "week_1": ["Review foundational concepts"],
                "week_2": ["Practice weak areas"],
                "week_3": ["Take mock assessments"],
                "week_4": ["Review and consolidate"]
            }
