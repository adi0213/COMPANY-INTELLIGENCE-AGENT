"""
Firecrawl API Collector

Scrapes a company's official homepage to extract raw Markdown.
This provides the LLM with the most accurate, ground-truth messaging directly from the company.
"""

import os
import aiohttp
import logging
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class FirecrawlCollector:
    def __init__(self):
        self.api_key = os.getenv("FIRECRAWL_API_KEY")

    async def collect_with_session(self, session: aiohttp.ClientSession, domain: str) -> Dict[str, Any]:
        """
        Scrapes the given domain and returns the raw markdown content.
        Requires the domain to be resolved by Hunter API first.
        """
        result = {
            "homepage_markdown": ""
        }

        if not self.api_key:
            logger.error("FIRECRAWL_API_KEY is missing from environment variables.")
            return result
            
        if not domain:
            logger.warning("No domain provided to Firecrawl. Skipping scrape.")
            return result

        url = "https://api.firecrawl.dev/v1/scrape"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Ensure domain has https://
        target_url = domain if domain.startswith("http") else f"https://{domain}"
        
        payload = {
            "url": target_url,
            "formats": ["markdown"],
            "onlyMainContent": True
        }

        try:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    markdown_content = data.get("data", {}).get("markdown", "")
                    
                    # Truncate if it's absurdly long to save vector space
                    if len(markdown_content) > 10000:
                        markdown_content = markdown_content[:10000]
                        
                    result["homepage_markdown"] = markdown_content
                    logger.info(f"Firecrawl: Successfully scraped {target_url} ({len(markdown_content)} chars)")
                else:
                    error_text = await response.text()
                    logger.warning(f"Firecrawl API returned {response.status} for {target_url}: {error_text}")
        except Exception as e:
            logger.error(f"Error calling Firecrawl API for {target_url}: {e}")

        return result
