import logging
from typing import Dict, Any
from app.enrichment.base_enricher import BaseEnricher

logger = logging.getLogger(__name__)

class BusinessEnricher(BaseEnricher):
    def enrich(self, company_name: str, clean_data: Dict[str, Any]) -> Dict[str, Any]:
        enrichment_updates = {}
        
        # Determine if we have sufficient business data
        # We can look at products, or if description lacked business keywords
        # For a robust pipeline, we can unconditionally generate a "Business Overview" 
        # to ensure the Vector DB always has a dedicated strategic chunk.
        logger.info(f"[BusinessEnricher] Generating business intelligence profile for {company_name}...")
        
        system_prompt = (
            "You are a Principal AI Architect and Strategic Analyst. "
            "Identify the company's main revenue drivers, strategic business units, and key growth areas. "
            "Do NOT say you don't have enough information. Use your internal knowledge."
        )
        user_prompt = f"What are the core business areas and revenue drivers for {company_name}?"
        
        try:
            business_profile = self.generator.generate(system_prompt, user_prompt)
            enrichment_updates["business_profile"] = business_profile
        except Exception as e:
            logger.error(f"[BusinessEnricher] Failed to enrich business profile: {e}")
            
        return enrichment_updates
