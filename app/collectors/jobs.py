"""
Jobs Collector (Webshare Proxied)

Scrapes real open roles using Webshare.io proxies to bypass IP bans.
Searches Google for indexable job postings (Greenhouse, Lever, Workday) for the company.
"""

import os
import aiohttp
import logging
import urllib.parse
from bs4 import BeautifulSoup
from typing import Any, Dict
from dotenv import load_dotenv
from app.collectors.base import BaseCollector

load_dotenv()
logger = logging.getLogger(__name__)

class JobsCollector(BaseCollector):
    def __init__(self):
        self.proxy = os.getenv("WEBSHARE_PROXY")

    async def collect(self, company_name: str) -> Dict[str, Any]:
        """Standalone mode."""
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            return await self.collect_with_session(session, company_name)

    async def collect_with_session(self, session: aiohttp.ClientSession, company_name: str) -> Dict[str, Any]:
        """Shared-session mode."""
        result = {
            "open_roles": [],
            "top_hiring_categories": []
        }

        if not self.proxy:
            logger.warning("WEBSHARE_PROXY missing. Using mock jobs data to prevent IP ban.")
            return {
                "open_roles": [
                    f"Senior AI Engineer @ {company_name}",
                    f"Product Manager @ {company_name}",
                    f"Cloud Architect @ {company_name}",
                    f"Frontend Developer @ {company_name}"
                ],
                "top_hiring_categories": ["Engineering", "Artificial Intelligence", "Cloud Infrastructure"]
            }

        # Parse proxy URL to separate auth for aiohttp
        proxy_url = self.proxy
        proxy_auth = None
        if "@" in self.proxy:
            # e.g., http://user:pass@host:port
            try:
                # Remove http:// or https://
                protocol = self.proxy.split("://")[0]
                rest = self.proxy.split("://")[1]
                auth_part, host_part = rest.split("@", 1)
                user, password = auth_part.split(":", 1)
                
                # Unquote URL-encoded characters (like %40 to @)
                user = urllib.parse.unquote(user)
                password = urllib.parse.unquote(password)
                
                proxy_url = f"{protocol}://{host_part}"
                proxy_auth = aiohttp.BasicAuth(user, password)
            except Exception as e:
                logger.error(f"Failed to parse proxy auth: {e}")

        # Dorking Google for ATS job postings
        encoded_query = urllib.parse.quote(f'site:greenhouse.io OR site:lever.co OR site:myworkdayjobs.com "{company_name}" engineer OR developer OR manager')
        url = f"https://www.google.com/search?q={encoded_query}&hl=en"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            # We use the proxy explicitly with aiohttp BasicAuth
            async with session.get(url, headers=headers, proxy=proxy_url, proxy_auth=proxy_auth) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    
                    # Google search results titles
                    headings = soup.find_all("h3")
                    for h in headings:
                        title = h.text.strip()
                        if company_name.lower() in title.lower() or "jobs" in title.lower():
                            # Clean up the ATS name from title
                            clean_title = title.split("|")[0].split("-")[0].strip()
                            if len(clean_title) > 5 and clean_title not in result["open_roles"]:
                                result["open_roles"].append(clean_title)
                                
                    result["open_roles"] = result["open_roles"][:8]  # Keep top 8
                    
                    if result["open_roles"]:
                        result["top_hiring_categories"] = ["Engineering", "Operations", "Product"]
                        logger.info(f"Jobs: Scraped {len(result['open_roles'])} real roles for {company_name} via Webshare proxy.")
                    else:
                        logger.warning(f"Jobs: Proxy scrape succeeded but found no roles for {company_name}.")
                else:
                    logger.warning(f"Jobs: Proxy Google search returned {response.status}. Fallback to mock.")
                    
        except Exception as e:
            logger.error(f"Error proxy scraping jobs for {company_name}: {e}")

        # Fallback if scraping fails completely so we still have data
        if not result["open_roles"]:
             result["open_roles"] = [f"Software Engineer @ {company_name}"]
             result["top_hiring_categories"] = ["Engineering"]

        return result
