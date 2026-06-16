"""
Products & Services Collector

Collects product and service info from Wikipedia.
Uses proper User-Agent header to avoid 403 responses.
"""

import aiohttp
import logging
import urllib.parse
from bs4 import BeautifulSoup
from typing import Any, Dict
from app.collectors.base import BaseCollector

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "CompanyIntelligenceAgent/1.0 (Research Project; your.email@example.com)"
}


class ProductsCollector(BaseCollector):

    async def collect(self, company_name: str) -> Dict[str, Any]:
        """Standalone mode."""
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout, headers=HEADERS) as session:
            return await self.collect_with_session(session, company_name)

    async def collect_with_session(self, session: aiohttp.ClientSession, company_name: str) -> Dict[str, Any]:
        """Shared-session mode."""
        result = {"products": [], "services": []}

        encoded_name = urllib.parse.quote(company_name.replace(" ", "_"))
        url = f"https://en.wikipedia.org/w/api.php?action=parse&page={encoded_name}&format=json&prop=text"

        try:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    data = await response.json()

                    if "parse" in data and "text" in data["parse"]:
                        html_content = data["parse"]["text"]["*"]
                        soup = BeautifulSoup(html_content, "html.parser")

                        headings = soup.find_all(["h2", "h3"])
                        for heading in headings:
                            heading_text = heading.text.lower()
                            if "product" in heading_text:
                                next_node = heading.find_next_sibling(["ul", "div"])
                                if next_node and next_node.name == "ul":
                                    items = next_node.find_all("li")
                                    result["products"].extend(
                                        [item.text.strip() for item in items[:5]]
                                    )
                            elif "service" in heading_text:
                                next_node = heading.find_next_sibling(["ul", "div"])
                                if next_node and next_node.name == "ul":
                                    items = next_node.find_all("li")
                                    result["services"].extend(
                                        [item.text.strip() for item in items[:5]]
                                    )

                    if not result["products"] and not result["services"]:
                        result["products"].append(
                            "Data not explicitly listed in structured format on Wikipedia."
                        )
                else:
                    logger.warning(
                        f"Wikipedia API returned {response.status} for {company_name} (Products)"
                    )
        except Exception as e:
            logger.error(f"Error fetching products for {company_name}: {e}")

        return result
