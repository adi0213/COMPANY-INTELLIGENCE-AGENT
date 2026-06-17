"""
Company Overview Collector

Collects high-level company details from the Wikipedia REST API.
Uses smart disambiguation to resolve company names (e.g. "Apple" → "Apple Inc.").
"""

import aiohttp
import logging
from typing import Any, Dict, List

from app.collectors.base import BaseCollector

logger = logging.getLogger(__name__)

# Wikipedia requires a meaningful User-Agent or returns 403
HEADERS = {
    "User-Agent": "CompanyIntelligenceAgent/1.0 (Research Project; your.email@example.com)"
}

# Common suffixes to try for disambiguation
COMPANY_SUFFIXES = [
    "_(company)", "_Inc.", "_(technology_company)", "_(software_company)",
    "_(conglomerate)", "_(corporation)", "_(brand)", "_(platform)",
    "_(service)", "_(organization)"
]


class CompanyOverviewCollector(BaseCollector):

    async def collect(self, company_name: str) -> Dict[str, Any]:
        """Standalone mode — creates its own session."""
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout, headers=HEADERS) as session:
            return await self.collect_with_session(session, company_name)

    async def collect_with_session(self, session: aiohttp.ClientSession, company_name: str) -> Dict[str, Any]:
        """Shared-session mode with smart disambiguation."""
        result = {
            "name": company_name,
            "industry": "",
            "headquarters": "",
            "description": "",
            "website": "",
            "employees": "",
            "founded": "",
        }

        safe_name = company_name.strip().replace(" ", "_")

        # Try disambiguation: "Apple_(company)", "Apple_Inc.", etc. before raw "Apple"
        candidates = [f"{safe_name}{suffix}" for suffix in COMPANY_SUFFIXES]
        candidates.append(safe_name)  # raw name as last resort

        best_description = ""
        best_title = ""

        for candidate in candidates:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{candidate}"
            try:
                async with session.get(url, headers=HEADERS) as response:
                    if response.status == 200:
                        data = await response.json()
                        extract = data.get("extract", "")
                        title = data.get("title", "")
                        page_type = data.get("type", "")

                        # Skip disambiguation pages
                        if page_type == "disambiguation" or "most often refers to:" in extract.lower() or "may refer to:" in extract.lower():
                            continue

                        # Heuristic: a company article usually mentions words like
                        # "company", "corporation", "founded", "headquartered", "CEO", "Inc."
                        company_signals = [
                            "company", "corporation", "inc.", "founded", "headquartered",
                            "multinational", "technology", "conglomerate", "enterprise",
                            "software", "ceo", "revenue", "nasdaq", "nyse", "stock",
                            "subsidiary", "parent company", "publicly traded"
                        ]
                        extract_lower = extract.lower()
                        signal_count = sum(1 for s in company_signals if s in extract_lower)

                        if signal_count >= 2:
                            # Strong company match — use it immediately
                            best_description = extract
                            best_title = title
                            logger.info(f"Wikipedia: Resolved '{company_name}' → '{candidate}' (signals: {signal_count})")
                            break
                        elif not best_description and len(extract) > 50:
                            # Weak match but better than nothing
                            best_description = extract
                            best_title = title

            except Exception as e:
                logger.warning(f"Wikipedia lookup failed for candidate '{candidate}': {e}")
                continue

        if best_description:
            result["description"] = best_description
            logger.info(f"Wikipedia: Final description for '{company_name}' ({len(best_description)} chars)")
        else:
            logger.warning(f"Wikipedia: No useful article found for '{company_name}'")

        return result
