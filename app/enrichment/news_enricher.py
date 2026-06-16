import logging
from typing import Dict, Any
from app.enrichment.base_enricher import BaseEnricher

logger = logging.getLogger(__name__)

class NewsEnricher(BaseEnricher):
    def enrich(self, company_name: str, clean_data: Dict[str, Any]) -> Dict[str, Any]:
        enrichment_updates = {}
        
        news = clean_data.get("news", [])
        
        if len(news) == 0:
            logger.info(f"[NewsEnricher] No news found for {company_name}. Synthesizing recent developments...")
            
            system_prompt = (
                "You are a tech journalist and market analyst. "
                "Describe the most recent major product launches, announcements, or AI initiatives "
                "by this company based on your training data up to the present. "
                "Do NOT say you don't have enough information. Use your internal knowledge."
            )
            user_prompt = f"What are the latest major developments and announcements for {company_name}?"
            
            try:
                news_profile = self.generator.generate(system_prompt, user_prompt)
                enrichment_updates["synthetic_news"] = news_profile
            except Exception as e:
                logger.error(f"[NewsEnricher] Failed to enrich news: {e}")
                
        return enrichment_updates
