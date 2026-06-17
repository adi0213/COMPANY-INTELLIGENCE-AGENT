"""
Hunter.io Collector

Uses the Hunter Domain Search API to resolve a company's official domain name
and extract key executives and personnel.
"""

import os
import aiohttp
import logging
import urllib.parse
from typing import Any, Dict
from dotenv import load_dotenv
from app.collectors.base import BaseCollector

load_dotenv()
logger = logging.getLogger(__name__)

class HunterCollector(BaseCollector):
    def __init__(self):
        self.api_key = os.getenv("HUNTER_API_KEY")

    async def collect(self, company_name: str) -> Dict[str, Any]:
        """Standalone mode."""
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            return await self.collect_with_session(session, company_name)

    async def collect_with_session(self, session: aiohttp.ClientSession, company_name: str) -> Dict[str, Any]:
        """Shared-session mode."""
        result = {
            "domain": "",
            "industry": "",
            "executives": []
        }

        if not self.api_key:
            logger.error("HUNTER_API_KEY is missing from environment variables.")
            return result

        encoded_name = urllib.parse.quote(company_name)
        url = f"https://api.hunter.io/v2/domain-search?company={encoded_name}&api_key={self.api_key}"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    data_obj = data.get("data", {})
                    
                    result["domain"] = data_obj.get("domain", "")
                    result["industry"] = data_obj.get("industry", "")
                    
                    # Extract executives or key roles from emails
                    emails = data_obj.get("emails", [])
                    executives = []
                    for email in emails:
                        position = email.get("position") or ""
                        first = email.get("first_name", "")
                        last = email.get("last_name", "")
                        
                        if position and first and last:
                            # Only grab senior roles or explicitly listed titles
                            if any(title in position.lower() for title in ["ceo", "cto", "cfo", "founder", "president", "director", "vp", "head"]):
                                executives.append(f"{first} {last} - {position}")
                    
                    result["executives"] = executives[:10]  # Cap at 10 to avoid token bloat
                    logger.info(f"Hunter API: Resolved domain '{result['domain']}' for '{company_name}'")
                else:
                    logger.warning(f"Hunter API returned {response.status} for {company_name}")
        except Exception as e:
            logger.error(f"Error calling Hunter API for {company_name}: {e}")

        return result
