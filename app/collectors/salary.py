"""
Salary Insights Collector

Why we need this:
- Compensation data gives insights into how a company values different departments.
- High ML Engineer salaries indicate a serious investment in AI.

Architecture & Design Decisions (Mock Implementation):
- Similar to Jobs, sites like Levels.fyi or Glassdoor are heavily guarded against scrapers.
- We are implementing a mock to fulfill the pipeline requirements. 

Future Scaling:
- To make this real later, you would likely need to purchase a data dump from a provider 
  or use an unofficial API endpoint discovered via browser dev tools (though this violates TOS).
- Storing this data locally is crucial because scraping it live every time a user requests 
  a company profile would be incredibly slow and likely get your IP banned.

Common Mistakes:
- Hitting guarded endpoints (like Glassdoor) too fast. If you ever scrape these for real, 
  you must use randomized delays, rotate proxies, and spoof User-Agent headers.
"""

import asyncio
import logging
from typing import Any, Dict
from app.collectors.base import BaseCollector

logger = logging.getLogger(__name__)

class SalaryCollector(BaseCollector):
    
    async def collect(self, company_name: str) -> Dict[str, Any]:
        """
        Mocks the collection of salary insights.
        """
        logger.info(f"Using mock SalaryCollector for {company_name}")
        
        # Simulate network delay
        await asyncio.sleep(1)
        
        # In reality, this data would be aggregated from multiple reports on a site like Levels.fyi
        
        return {
            "software_engineer": "$150,000 - $250,000",
            "data_scientist": "$140,000 - $230,000",
            "ml_engineer": "$180,000 - $300,000",
            "product_manager": "$130,000 - $210,000"
        }
