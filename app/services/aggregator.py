"""
Aggregator Service

Orchestrates all collectors concurrently using a single shared aiohttp session
to prevent socket exhaustion on Windows.
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

from app.utils.storage import save_raw_data
from app.evaluation.latency_tracker import track_latency

logger = logging.getLogger(__name__)


@track_latency(endpoint_name="Collection")
async def collect_company_data(company_name: str) -> Dict[str, Any]:
    """
    Runs all collectors concurrently with a SINGLE shared aiohttp session.
    This prevents socket exhaustion (WinError 10055) by reusing TCP connections.
    """
    logger.info(f"Starting data collection for {company_name}")

    timeout = aiohttp.ClientTimeout(total=15, connect=5)
    connector = aiohttp.TCPConnector(limit=5, force_close=True)
    headers = {"User-Agent": "CompanyIntelligenceAgent/1.0 (Research Project; your.email@example.com)"}

    async with aiohttp.ClientSession(timeout=timeout, connector=connector, headers=headers) as session:
        co_collector = CompanyOverviewCollector()
        news_collector = NewsCollector()
        jobs_collector = JobsCollector()
        salary_collector = SalaryCollector()
        products_collector = ProductsCollector()

        results = await asyncio.gather(
            co_collector.collect_with_session(session, company_name),
            news_collector.collect_with_session(session, company_name),
            jobs_collector.collect(company_name),
            salary_collector.collect(company_name),
            products_collector.collect_with_session(session, company_name),
            return_exceptions=True,
        )

    company_data, news_data, jobs_data, salary_data, products_data = results

    def get_valid_data(data, default_type):
        if isinstance(data, Exception):
            logger.error(f"Collector failed: {data}")
            return default_type()
        return data

    payload = {
        "company": get_valid_data(company_data, dict),
        "news": get_valid_data(news_data, list),
        "jobs": get_valid_data(jobs_data, dict),
        "salary": get_valid_data(salary_data, dict),
        "products": get_valid_data(products_data, dict),
    }

    try:
        save_raw_data(company_name, payload)
    except Exception as e:
        logger.error(f"Could not save payload to disk: {e}")

    logger.info(f"Successfully completed data collection for {company_name}")
    return payload
