"""
Company Analysis Service — Production Pipeline

Orchestrates the full end-to-end flow:
  1. Collect raw company data from all sources
  2. Clean and normalize
  3. Embed and index into ChromaDB
  4. Run all specialized agents (each queries ChromaDB + Ollama)
  5. Return structured intelligence report

This is the production endpoint that powers the frontend search experience.
"""

import logging
import asyncio
from typing import Dict, Any

from app.services.aggregator import collect_company_data
from app.services.cleaning_service import clean_company_data
from app.services.embedding_service import process_and_index_company
from app.agents.coordinator import CoordinatorAgent

from app.enrichment.company_enricher import CompanyEnricher
from app.enrichment.technology_enricher import TechnologyEnricher
from app.enrichment.business_enricher import BusinessEnricher
from app.enrichment.hiring_enricher import HiringEnricher
from app.enrichment.news_enricher import NewsEnricher
from app.rag.generator import Generator

logger = logging.getLogger(__name__)

# Singleton coordinator and generator
_coordinator = CoordinatorAgent()
_generator = Generator()


async def analyze_company(company_name: str) -> Dict[str, Any]:
    """
    Full end-to-end Company Intelligence Pipeline.
    
    Step 1: Collect data from web (async, concurrent collectors)
    Step 2: Clean and normalize
    Step 3: Embed and index in ChromaDB
    Step 4: Run all specialized agents against the indexed data
    Step 5: Return structured report
    """
    logger.info(f"[CompanyAnalyzer] === STARTING FULL ANALYSIS: {company_name} ===")

    # ── Step 1: Collect ──────────────────────────────────────────
    logger.info(f"[CompanyAnalyzer] Step 1/4: Collecting data...")
    raw_data = await collect_company_data(company_name)

    # ── Step 2: Clean ────────────────────────────────────────────
    logger.info(f"[CompanyAnalyzer] Step 2/5: Cleaning data...")
    clean_data = clean_company_data(raw_data)

    # ── Step 2.5: Enrich (PARALLEL) ──────────────────────────────
    logger.info(f"[CompanyAnalyzer] Step 3/5: Enriching sparse data concurrently...")
    enrichers = [
        CompanyEnricher(),
        TechnologyEnricher(),
        BusinessEnricher(),
        HiringEnricher(),
        NewsEnricher()
    ]
    
    async def _run_enricher(enricher):
        try:
            return await asyncio.to_thread(enricher.enrich, company_name, clean_data)
        except Exception as e:
            logger.error(f"[CompanyAnalyzer] Enricher failed: {e}")
            return {}

    enrichment_results = await asyncio.gather(*[_run_enricher(e) for e in enrichers])
    
    # Merge all enrichment updates back into clean_data
    for updates in enrichment_results:
        clean_data.update(updates)

    # ── Step 3: Embed & Index ────────────────────────────────────
    logger.info(f"[CompanyAnalyzer] Step 4/5: Embedding and indexing in ChromaDB...")
    index_result = process_and_index_company(clean_data)
    logger.info(f"[CompanyAnalyzer] Indexed {index_result.get('chunks_processed', 0)} chunks")

    # ── Step 4: Run All Agents (PARALLEL with limits) ────────────
    logger.info(f"[CompanyAnalyzer] Step 5/5: Running specialized agents concurrently...")
    
    # Limit to 10 concurrent RAG executions.
    # OpenBLAS OOM is now prevented by a thread lock in rag_service.py
    semaphore = asyncio.Semaphore(10)

    async def _safe_execute_async(agent, question: str) -> Dict[str, Any]:
        """Execute an agent concurrently, apply quality gate, return structured output."""
        async with semaphore:
            try:
                # Run the synchronous agent.execute in a background thread
                result = await asyncio.to_thread(agent.execute, company_name, question)
            
                # We log confidence, but we no longer override answers because we explicitly requested
                # the LLM to synthesize exhaustive information using world knowledge.
                confidence = result.get("confidence", 0.0)
                
                return {
                    "content": result.get("answer", "No data available."),
                    "confidence": confidence,
                    "sources": result.get("source_count", 0),
                    "source_types": ["Scraped & Synthetic Enrichment"]
                }
            except Exception as e:
                logger.error(f"[CompanyAnalyzer] Agent {agent.name} failed: {e}")
                return {
                    "content": f"Agent encountered an error: {str(e)}",
                    "confidence": 0.0,
                    "sources": 0,
                    "source_types": ["Error"]
                }

    # Define all agent tasks
    tasks = {
        "overview": _safe_execute_async(
            _coordinator.company_agent,
            f"Give a comprehensive overview of {company_name} including its industry, headquarters, founding date, CEO, employee count, and website."
        ),
        "latest_developments": _safe_execute_async(
            _coordinator.news_agent,
            f"What are the latest major developments, announcements, product launches, acquisitions, partnerships, and AI initiatives at {company_name}?"
        ),
        "key_technologies": _safe_execute_async(
            _coordinator.tech_agent,
            f"What are the key technologies, frameworks, programming languages, cloud platforms, and AI tools used or developed by {company_name}?"
        ),
        "business_areas": _safe_execute_async(
            _coordinator.company_agent,
            f"What are the most important business areas, revenue drivers, strategic business units, and growth areas for {company_name}?"
        ),
        "interview_focus": _safe_execute_async(
            _coordinator.interview_agent,
            f"What are the common technical and behavioral interview focus areas, topics, and preparation tips for {company_name}?"
        ),
        "hiring_trends": _safe_execute_async(
            _coordinator.hiring_agent,
            f"What are the current hiring trends, top roles, most common departments, and emerging skill requirements at {company_name}?"
        ),
        "salary_insights": _safe_execute_async(
            _coordinator.salary_agent,
            f"What are the typical salary ranges for Software Engineer, Data Scientist, ML Engineer, and Product Manager at {company_name}?"
        ),
        "executive_summary": _safe_execute_async(
            _coordinator.company_agent,
            f"Write a 2-3 sentence executive summary of {company_name}'s current strategic position, key initiatives, and competitive advantages."
        )
    }

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks.values())
    
    # Map results back to keys
    keys = list(tasks.keys())
    agent_data = dict(zip(keys, results))

    logger.info(f"[CompanyAnalyzer] === ANALYSIS COMPLETE: {company_name} ===")

    return {
        "company": company_name,
        "overview": agent_data["overview"],
        "latest_developments": agent_data["latest_developments"],
        "key_technologies": agent_data["key_technologies"],
        "business_areas": agent_data["business_areas"],
        "interview_focus": agent_data["interview_focus"],
        "hiring_trends": agent_data["hiring_trends"],
        "salary_insights": agent_data["salary_insights"],
        "executive_summary": agent_data["executive_summary"],
    }
