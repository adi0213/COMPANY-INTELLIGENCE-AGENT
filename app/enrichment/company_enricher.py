import logging
from typing import Dict, Any
from app.enrichment.base_enricher import BaseEnricher

logger = logging.getLogger(__name__)

class CompanyEnricher(BaseEnricher):
    def enrich(self, company_name: str, clean_data: Dict[str, Any]) -> Dict[str, Any]:
        company_info = clean_data.get("company", {})
        description = company_info.get("description", "").strip()
        
        enrichment_updates = {}
        
        # If description is too short or missing
        if len(description) < 50:
            logger.info(f"[CompanyEnricher] Missing or sparse description for {company_name}. Synthesizing from world knowledge...")
            
            system_prompt = (
                "You are an expert corporate intelligence analyst. "
                "Provide a highly accurate, comprehensive company overview. "
                "Include the company's mission, main products/services, industry, and business model. "
                "Do NOT say you don't have enough information. Use your internal knowledge."
            )
            user_prompt = f"Write a detailed, formal company description for {company_name}."
            
            try:
                enriched_desc = self.generator.generate(system_prompt, user_prompt)
                enrichment_updates["description"] = enriched_desc
                enrichment_updates["enriched_description"] = True
            except Exception as e:
                logger.error(f"[CompanyEnricher] Failed to enrich company description: {e}")
                
        return enrichment_updates
