import logging
from typing import Dict, Any
from app.enrichment.base_enricher import BaseEnricher

logger = logging.getLogger(__name__)

class TechnologyEnricher(BaseEnricher):
    def enrich(self, company_name: str, clean_data: Dict[str, Any]) -> Dict[str, Any]:
        enrichment_updates = {}
        
        # Check if we have explicit tech stack information
        products = clean_data.get("products", {})
        services = products.get("services", [])
        
        # If products/services are sparse, we synthesize a technology footprint
        if len(services) < 2:
            logger.info(f"[TechnologyEnricher] Sparse technology data for {company_name}. Synthesizing...")
            
            system_prompt = (
                "You are a Staff Data Engineer and Enterprise Search Engineer. "
                "List the primary technologies, frameworks, cloud platforms, programming languages, "
                "and AI tools known to be used or developed by this company. "
                "Provide a structured, comma-separated list or short paragraphs."
                "Do NOT say you don't have enough information. Use your internal knowledge."
            )
            user_prompt = f"What is the technology stack and key technical platforms of {company_name}?"
            
            try:
                tech_stack = self.generator.generate(system_prompt, user_prompt)
                # Instead of modifying existing lists blindly, we attach a new explicit tech stack section
                enrichment_updates["inferred_tech_stack"] = tech_stack
            except Exception as e:
                logger.error(f"[TechnologyEnricher] Failed to enrich tech stack: {e}")
                
        return enrichment_updates
