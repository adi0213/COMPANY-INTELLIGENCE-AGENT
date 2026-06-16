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

    # ── Step 2.5: Enrich ─────────────────────────────────────────
    logger.info(f"[CompanyAnalyzer] Step 3/5: Enriching sparse data...")
    enrichers = [
        CompanyEnricher(),
        TechnologyEnricher(),
        BusinessEnricher(),
        HiringEnricher(),
        NewsEnricher()
    ]
    for enricher in enrichers:
        try:
            updates = enricher.enrich(company_name, clean_data)
            clean_data.update(updates)
        except Exception as e:
            logger.error(f"[CompanyAnalyzer] Enricher failed: {e}")

    # ── Step 3: Embed & Index ────────────────────────────────────
    logger.info(f"[CompanyAnalyzer] Step 4/5: Embedding and indexing in ChromaDB...")
    index_result = process_and_index_company(clean_data)
    logger.info(f"[CompanyAnalyzer] Indexed {index_result.get('chunks_processed', 0)} chunks")

    # ── Step 4: Run All Agents ───────────────────────────────────
    logger.info(f"[CompanyAnalyzer] Step 5/5: Running specialized agents...")

    def _safe_execute(agent, question: str) -> Dict[str, Any]:
        """Execute an agent, apply quality gate, return structured output."""
        try:
            result = agent.execute(company_name, question)
            
            # QUALITY GATE: If confidence is very low, synthesize from world knowledge directly
            confidence = result.get("confidence", 0.0)
            if confidence < 0.2:
                logger.warning(f"[QualityGate] {agent.name} failed confidence threshold ({confidence}). Invoking LLM fallback...")
                system_prompt = "You are an expert analyst. Answer comprehensively using internal knowledge. Do not say you lack info."
                new_answer = _generator.generate(system_prompt, question)
                return {
                    "content": new_answer,
                    "confidence": 0.2, # Minimum synthetic confidence
                    "sources": 0,
                    "source_types": ["LLM Synthesis"]
                }
                
            return {
                "content": result.get("answer", "No data available."),
                "confidence": confidence,
                "sources": result.get("source_count", 0),
                "source_types": ["Scraped Context"] if result.get("source_count", 0) > 0 else ["Fallback"]
            }
        except Exception as e:
            logger.error(f"[CompanyAnalyzer] Agent {agent.name} failed: {e}")
            return {
                "content": f"Agent encountered an error: {str(e)}",
                "confidence": 0.0,
                "sources": 0,
                "source_types": ["Error"]
            }

    overview_data = _safe_execute(
        _coordinator.company_agent,
        f"Give a comprehensive overview of {company_name} including its industry, headquarters, founding date, CEO, employee count, and website."
    )

    news_data = _safe_execute(
        _coordinator.news_agent,
        f"What are the latest major developments, announcements, product launches, acquisitions, partnerships, and AI initiatives at {company_name}?"
    )

    tech_data = _safe_execute(
        _coordinator.tech_agent,
        f"What are the key technologies, frameworks, programming languages, cloud platforms, and AI tools used or developed by {company_name}?"
    )

    business_data = _safe_execute(
        _coordinator.company_agent,
        f"What are the most important business areas, revenue drivers, strategic business units, and growth areas for {company_name}?"
    )

    interview_data = _safe_execute(
        _coordinator.interview_agent,
        f"What are the common technical and behavioral interview focus areas, topics, and preparation tips for {company_name}?"
    )

    hiring_data = _safe_execute(
        _coordinator.hiring_agent,
        f"What are the current hiring trends, top roles, most common departments, and emerging skill requirements at {company_name}?"
    )

    salary_data = _safe_execute(
        _coordinator.salary_agent,
        f"What are the typical salary ranges for Software Engineer, Data Scientist, ML Engineer, and Product Manager at {company_name}?"
    )

    summary_data = _safe_execute(
        _coordinator.company_agent,
        f"Write a 2-3 sentence executive summary of {company_name}'s current strategic position, key initiatives, and competitive advantages."
    )

    logger.info(f"[CompanyAnalyzer] === ANALYSIS COMPLETE: {company_name} ===")

    return {
        "company": company_name,
        "overview": overview_data,
        "latest_developments": news_data,
        "key_technologies": tech_data,
        "business_areas": business_data,
        "interview_focus": interview_data,
        "hiring_trends": hiring_data,
        "salary_insights": salary_data,
        "executive_summary": summary_data,
    }
