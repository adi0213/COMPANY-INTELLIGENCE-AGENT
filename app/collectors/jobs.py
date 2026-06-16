"""
Hiring Trends Collector

Why we need this:
- Job postings are a strong leading indicator of a company's strategic direction.
- Are they hiring lots of AI Engineers? That tells the LLM they are pivoting to AI.
- Are they freezing hiring? That signals financial caution.

Architecture & Design Decisions (Mock Implementation):
- Scraping job boards (LinkedIn, Greenhouse, Workday) is notoriously difficult.
  They use aggressive bot-protection (Cloudflare, CAPTCHAs) and heavily obfuscated JavaScript.
- To maintain momentum in Phase 2, we are building a "Mock" collector. 
  It conforms to our BaseCollector interface. Later, you can swap the internals of `collect()` 
  with a paid API (like the LinkedIn Jobs API or a proxy service like BrightData) without 
  breaking the rest of your application.

Industry Best Practice:
- When dealing with unreliable scraping targets, use the "Adapter Pattern". This collector 
  acts as an adapter. The system doesn't care *how* it gets the jobs, just that it returns 
  the standard dictionary format.
"""

import asyncio
import logging
from typing import Any, Dict
from app.collectors.base import BaseCollector

logger = logging.getLogger(__name__)

class JobsCollector(BaseCollector):
    
    async def collect(self, company_name: str) -> Dict[str, Any]:
        """
        Mocks the collection of hiring trends.
        """
        logger.info(f"Using mock JobsCollector for {company_name}")
        
        # Simulate network latency (e.g., waiting for a Headless Chrome instance to load)
        await asyncio.sleep(1)
        
        # In a real scenario, we might scrape LinkedIn Jobs or a company's career page
        # and parse the titles to categorize them.
        
        return {
            "open_roles": [
                f"Senior AI Engineer @ {company_name}",
                f"Product Manager @ {company_name}",
                f"Cloud Architect @ {company_name}",
                f"Frontend Developer @ {company_name}"
            ],
            "top_hiring_categories": [
                "Engineering",
                "Artificial Intelligence",
                "Cloud Infrastructure"
            ]
        }
