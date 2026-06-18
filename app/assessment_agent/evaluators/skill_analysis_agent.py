import json
import logging
from typing import Dict, Any

from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class SkillAnalysisAgent:
    def __init__(self):
        self.generator = Generator()

    def analyze_skills(self, assessment_type: str, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze strengths and weaknesses based on raw evaluation results.
        Returns a dict matching the SkillAnalysis schema.
        """
        system_prompt = (
            "You are an expert technical assessor and career coach. "
            "Given the raw scores and results of an assessment, analyze the candidate's skills. "
            "Identify their top strengths, primary weaknesses, and key focus areas for improvement. "
            "Return ONLY valid JSON format. The response must be a JSON object containing exactly these keys: "
            "'strengths' (list of strings), 'weaknesses' (list of strings), 'focus_areas' (list of strings)."
        )

        user_prompt = f"Assessment Type: {assessment_type}\n\nRaw Results:\n{json.dumps(raw_results, indent=2)}\n\nGenerate the skill analysis JSON."

        try:
            import re
            response = self.generator.generate(system_prompt, user_prompt, json_mode=True)
            
            # Use regex to robustly extract JSON object
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = "{}"

            analysis = json.loads(json_str)
            
            # Validation
            required_keys = ['strengths', 'weaknesses', 'focus_areas']
            for key in required_keys:
                if key not in analysis:
                    analysis[key] = []
                    
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing skills: {e}")
            return {
                "strengths": ["Unable to determine strengths"],
                "weaknesses": ["Unable to determine weaknesses"],
                "focus_areas": ["General practice recommended"]
            }
