"""
RAG Service Orchestrator

Why we need this:
- We have 6 independent RAG modules. We need a "Conductor" to orchestrate them in the correct order.
- This is the entry point for the FastAPI endpoints.

Workflow:
User Query -> Retriever -> Reranker -> Context Builder -> Prompt Builder -> LLM Generator
                                                        -> Source Manager
"""

import logging
from typing import Dict, Any, List

from app.rag.retriever import Retriever
from app.rag.reranker import Reranker
from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import PromptBuilder
from app.rag.generator import Generator
from app.rag.source_manager import SourceManager

logger = logging.getLogger(__name__)

from app.evaluation.latency_tracker import track_latency
from app.evaluation.rag_metrics import evaluate_rag_output
from app.evaluation.db import log_evaluation

# Initialize Agent Singletons
retriever = Retriever(top_k=20)
reranker = Reranker(top_k=5)
context_builder = ContextBuilder()
prompt_builder = PromptBuilder()

# Connect to OpenRouter (or fallback chain)
generator = Generator(model="llama3.1")

source_manager = SourceManager()

@track_latency(endpoint_name="execute_rag_pipeline")
def execute_rag_pipeline(company_name: str, question: str) -> Dict[str, Any]:
    """
    Executes the full Retrieval-Augmented Generation pipeline.
    
    KEY CHANGE: Even when no chunks are retrieved, we still call the LLM 
    so it can answer using its own world knowledge. We never return 
    "no data available" to the user.
    """
    logger.info(f"Executing RAG pipeline for company: {company_name}")
    
    # 1. Retrieve (High Recall)
    # Filter metadata to only search documents belonging to this specific company
    filter_metadata = {"company": company_name} if company_name else None
    raw_chunks = retriever.retrieve(question, filter_metadata=filter_metadata)
    
    # 2. Rerank (High Precision)
    top_chunks = reranker.rerank(question, raw_chunks)
    
    # 3. Build Context (even if empty — the LLM will use world knowledge)
    context_str = context_builder.build_context(top_chunks)
        
    # 4. Build Prompts
    system_prompt = prompt_builder.get_system_prompt()
    user_prompt = prompt_builder.build_user_prompt(question, context_str)
    
    # 5. Generate Answer (LLM will supplement with world knowledge if context is sparse)
    answer = generator.generate(system_prompt, user_prompt)
    
    # 6. Extract Sources
    sources = source_manager.extract_sources(top_chunks) if top_chunks else []
    
    # 7. Quality Evaluation (lightweight heuristic, no extra LLM call)
    hallucination_score = evaluate_rag_output(context_str, answer)
    faithfulness_score = hallucination_score
    
    # Log the evaluation to our SQLite Telemetry Database
    agent_name = "BaseRAG"
    log_evaluation(question, agent_name, len(top_chunks), hallucination_score, faithfulness_score)
    
    return {
        "answer": answer,
        "sources": sources,
        "confidence": faithfulness_score,
        "source_count": len(sources)
    }

def execute_debug_rag(query: str) -> Dict[str, Any]:
    """
    Executes a partial pipeline returning the raw intermediate steps so 
    engineers can see what the Vector DB and Reranker are actually doing.
    """
    logger.info(f"Executing Debug RAG for query: {query}")
    
    raw_chunks = retriever.retrieve(query)
    top_chunks = reranker.rerank(query, raw_chunks)
    context_str = context_builder.build_context(top_chunks)
    
    return {
        "retrieved_chunks": raw_chunks,
        "reranked_chunks": top_chunks,
        "final_context": context_str
    }
