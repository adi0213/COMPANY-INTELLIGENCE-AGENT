"""
News Collector

Collects recent news articles using Google News RSS feeds.
Uses html.parser instead of lxml's xml parser to avoid dependency issues.
"""

import aiohttp
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import logging
import urllib.parse
from typing import Any, Dict, List
from app.collectors.base import BaseCollector

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "CompanyIntelligenceAgent/1.0 (Research Project; your.email@example.com)"
}


class NewsCollector(BaseCollector):

    async def collect(self, company_name: str) -> List[Dict[str, str]]:
        """Standalone mode."""
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout, headers=HEADERS) as session:
            return await self.collect_with_session(session, company_name)

    async def collect_with_session(self, session: aiohttp.ClientSession, company_name: str) -> List[Dict[str, str]]:
        """Shared-session mode."""
        news_items = []

        encoded_query = urllib.parse.quote(f"{company_name} company")
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

        try:
            async with session.get(rss_url, headers=HEADERS) as response:
                if response.status == 200:
                    xml_content = await response.text()
                    # Use html.parser as a safe fallback — works without lxml installed
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
                        soup = BeautifulSoup(xml_content, features="html.parser")
                    items = soup.find_all("item")

                    for item in items[:10]:
                        title = item.find("title")
                        link = item.find("link")
                        pub_date = item.find("pubdate")
                        source = item.find("source")

                        news_items.append({
                            "title": title.text.strip() if title else "",
                            "source": source.text.strip() if source else "Google News",
                            "date": pub_date.text.strip() if pub_date else "",
                            "link": link.text.strip() if link else "",
                        })
                else:
                    logger.warning(f"Google News RSS returned {response.status} for {company_name}")

        except Exception as e:
            logger.error(f"Error fetching news for {company_name}: {e}")

        return news_items
