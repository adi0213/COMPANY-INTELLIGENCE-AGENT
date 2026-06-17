"""
Aggregator Service

Orchestrates all collectors concurrently using a shared aiohttp session.
Integrates premium data sources (Hunter, Firecrawl) alongside traditional scrapers.
"""

import asyncio
import aiohttp
import logging
from typing import Any, Dict

from app.collectors.company import CompanyOverviewCollector
from app.collectors.news import NewsCollector
from app.collectors.jobs import JobsCollector
from app.collectors.salary import SalaryCollector
from app.collectors.products import ProductsCollector
from app.collectors.hunter import HunterCollector
from app.collectors.firecrawl import FirecrawlCollector

from app.utils.storage import save_raw_data
from app.evaluation.latency_tracker import track_latency

logger = logging.getLogger(__name__)

async def _fetch_hunter_and_firecrawl(session: aiohttp.ClientSession, company_name: str) -> tuple:
    """
    Helper to run Hunter and then Firecrawl sequentially, since Firecrawl needs the domain.
    """
    hunter = HunterCollector()
    firecrawl = FirecrawlCollector()
    
    # 1. Fetch from Hunter to get the domain
    hunter_data = await hunter.collect_with_session(session, company_name)
    domain = hunter_data.get("domain", "")
    
    # 2. Fetch from Firecrawl using the domain
    firecrawl_data = {}
    if domain:
        firecrawl_data = await firecrawl.collect_with_session(session, domain)
        
    return hunter_data, firecrawl_data

@track_latency(endpoint_name="Collection")
async def collect_company_data(company_name: str) -> Dict[str, Any]:
    """
    Runs all collectors concurrently.
    """
    logger.info(f"Starting premium data collection for {company_name}")

    # Increased timeout since Firecrawl and proxy scrape can take longer
    timeout = aiohttp.ClientTimeout(total=30, connect=10)
    connector = aiohttp.TCPConnector(limit=5, force_close=True)
    headers = {"User-Agent": "CompanyIntelligenceAgent/1.0 (Research Project)"}

    async with aiohttp.ClientSession(timeout=timeout, connector=connector, headers=headers) as session:
        co_collector = CompanyOverviewCollector()
        news_collector = NewsCollector()
        jobs_collector = JobsCollector()
        salary_collector = SalaryCollector()
        products_collector = ProductsCollector()

        # Run the standard collectors alongside the chained Hunter->Firecrawl
        results = await asyncio.gather(
            co_collector.collect_with_session(session, company_name),
            news_collector.collect_with_session(session, company_name),
            jobs_collector.collect_with_session(session, company_name),
            salary_collector.collect(company_name),
            products_collector.collect_with_session(session, company_name),
            _fetch_hunter_and_firecrawl(session, company_name),
            return_exceptions=True,
        )

    company_data = results[0]
    news_data = results[1]
    jobs_data = results[2]
    salary_data = results[3]
    products_data = results[4]
    hunter_firecrawl_data = results[5]

    def get_valid_data(data, default_type):
        if isinstance(data, Exception):
            logger.error(f"Collector failed: {data}")
            return default_type()
        return data

    company_valid = get_valid_data(company_data, dict)
    hunter_firecrawl_valid = get_valid_data(hunter_firecrawl_data, lambda: ({}, {}))
    
    hunter_dict = hunter_firecrawl_valid[0] if isinstance(hunter_firecrawl_valid, tuple) else {}
    firecrawl_dict = hunter_firecrawl_valid[1] if isinstance(hunter_firecrawl_valid, tuple) else {}
    
    # Merge Hunter data into company_valid
    if hunter_dict:
        company_valid["domain"] = hunter_dict.get("domain", "")
        if hunter_dict.get("industry") and not company_valid.get("industry"):
             company_valid["industry"] = hunter_dict["industry"]
        company_valid["executives"] = hunter_dict.get("executives", [])

    payload = {
        "company": company_valid,
        "news": get_valid_data(news_data, list),
        "jobs": get_valid_data(jobs_data, dict),
        "salary": get_valid_data(salary_data, dict),
        "products": get_valid_data(products_data, dict),
        "firecrawl": firecrawl_dict
    }

    try:
        save_raw_data(company_name, payload)
    except Exception as e:
        logger.error(f"Could not save payload to disk: {e}")

    logger.info(f"Successfully completed premium collection for {company_name}")
    return payload
