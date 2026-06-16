"""
Company Overview Collector

Collects high-level company details from the Wikipedia REST API.
Uses a proper User-Agent header (required by Wikipedia API policy).
"""

import aiohttp
import logging
from typing import Any, Dict
from app.collectors.base import BaseCollector

logger = logging.getLogger(__name__)

# Wikipedia requires a meaningful User-Agent or returns 403
HEADERS = {
    "User-Agent": "CompanyIntelligenceAgent/1.0 (Research Project; your.email@example.com)"
}


class CompanyOverviewCollector(BaseCollector):

    async def collect(self, company_name: str) -> Dict[str, Any]:
        """Standalone mode — creates its own session."""
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout, headers=HEADERS) as session:
            return await self.collect_with_session(session, company_name)

    async def collect_with_session(self, session: aiohttp.ClientSession, company_name: str) -> Dict[str, Any]:
        """Shared-session mode."""
        result = {
            "name": company_name,
            "industry": "",
            "headquarters": "",
            "description": "",
            "website": "",
            "employees": "",
            "founded": "",
        }

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company_name.replace(' ', '_')}"

        try:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    data = await response.json()
                    result["description"] = data.get("extract", "")
                else:
                    logger.warning(f"Wikipedia API returned {response.status} for {company_name}")
        except Exception as e:
            logger.error(f"Error fetching company overview for {company_name}: {e}")

        return result
