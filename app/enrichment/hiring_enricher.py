import logging
from typing import Dict, Any
from app.enrichment.base_enricher import BaseEnricher

logger = logging.getLogger(__name__)

class HiringEnricher(BaseEnricher):
    def enrich(self, company_name: str, clean_data: Dict[str, Any]) -> Dict[str, Any]:
        enrichment_updates = {}
        
        jobs = clean_data.get("jobs", {}).get("open_roles", [])
        
        if len(jobs) < 2:
            logger.info(f"[HiringEnricher] Sparse hiring data for {company_name}. Synthesizing...")
            
            system_prompt = (
                "You are an expert tech recruiter and talent acquisition analyst. "
                "Describe the current hiring trends, most common engineering departments, "
                "and typical open roles for this company. "
                "Do NOT say you don't have enough information. Use your internal knowledge."
            )
            user_prompt = f"What are the typical open roles and hiring trends at {company_name}?"
            
            try:
                hiring_profile = self.generator.generate(system_prompt, user_prompt)
                enrichment_updates["hiring_profile"] = hiring_profile
            except Exception as e:
                logger.error(f"[HiringEnricher] Failed to enrich hiring profile: {e}")
                
        return enrichment_updates
