"""
API Routes definition for the Company Intelligence Agent.

Why we need this:
- This file defines the endpoints (URLs) that clients can interact with.
- It maps HTTP methods (GET, POST, etc.) to Python functions.

Architecture & Design Decisions:
- We use `APIRouter` to group related endpoints. This is then imported and included in `main.py`.
- The route acts purely as a "Controller" (in MVC terms) or "Delivery Mechanism". 
  It takes the input (`company_name`), passes it to the `Service` layer, and returns the result.
- Notice that there is NO scraping or data aggregation logic here. This keeps the code testable and modular.

Future Scalability:
- When we add endpoints to trigger specific pipelines (e.g., POST /pipeline/clean), they will live in dedicated routers.

Common Mistakes:
- Doing I/O operations (like fetching from web or saving to disk) directly inside the route function. Always delegate to a service!
"""

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from typing import Optional, Dict, Any

from typing import Optional, Dict, Any

from app.services.aggregator import collect_company_data
from app.services.cleaning_service import clean_company_data
from app.services.embedding_service import process_and_index_company
from app.vector_db.search import semantic_search
from app.services.rag_service import execute_rag_pipeline, execute_debug_rag
router = APIRouter(
    tags=["Company Data Collection"]
)

@router.get("/company/{company_name}")
async def get_company_data(
    company_name: str = Path(..., title="The name of the company to collect data for", example="Google")
):
    """
    Orchestrates the collection of data for a given company.
    """
    try:
        result = await collect_company_data(company_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/company/{company_name}/clean")
async def get_cleaned_company_data(
    company_name: str = Path(..., title="The name of the company to clean data for", example="Google")
):
    """
    Orchestrates both the collection AND cleaning of data for a given company.
    
    Workflow:
    1. Awaits the raw data collection.
    2. Passes the raw JSON through the cleaning pipeline synchronously.
    3. Returns the clean JSON.
    """
    try:
        # Step 1: Collect
        raw_data = await collect_company_data(company_name)
        
        # Step 2: Clean
        clean_data = clean_company_data(raw_data)
        
        return clean_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SearchRequest(BaseModel):
    query: str
    n_results: int = 5
    filter_metadata: Optional[Dict[str, Any]] = None

class AskRequest(BaseModel):
    company: str
    question: str

class DebugRagRequest(BaseModel):
    query: str

@router.get("/company/{company_name}/embeddings")
async def generate_company_embeddings(
    company_name: str = Path(..., title="The name of the company to index", examples=["Google"])
):
    """
    End-to-End Pipeline: Fetch -> Clean -> Embed -> Index in ChromaDB.
    """
    try:
        raw_data = await collect_company_data(company_name)
        clean_data = clean_company_data(raw_data)
        
        # Phase 4/5: Embed and Index
        result = process_and_index_company(clean_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_company_data(request: SearchRequest):
    """
    Semantic Search using Vector Database.
    """
    try:
        results = semantic_search(
            query=request.query, 
            n_results=request.n_results, 
            filter_metadata=request.filter_metadata
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
async def ask_company_question(request: AskRequest):
    """
    RAG Endpoint. Given a company name and a question, retrieves context 
    from the Vector DB and uses an LLM to generate a grounded answer.
    """
    try:
        result = execute_rag_pipeline(request.company, request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/debug-rag")
async def debug_rag_pipeline(request: DebugRagRequest):
    """
    Returns the intermediate retrieval and reranking steps so you can 
    see exactly what the Vector DB returned before it was sent to the LLM.
    """
    try:
        result = execute_debug_rag(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from app.agents.coordinator import CoordinatorAgent
from app.agents.aggregator import AggregatorAgent

# Initialize Agent Singletons
coordinator = CoordinatorAgent()
aggregator = AggregatorAgent()

@router.post("/agent-ask")
async def agent_ask_question(request: AskRequest):
    """
    Multi-Agent Endpoint.
    Routes the question to specialized agents and aggregates their answers.
    """
    try:
        # 1. Coordinate (Semantic Routing)
        assigned_agents = coordinator.route_query(request.question)
        
        # 2. Execute parallel/sequential agent tasks
        agent_results = []
        for agent in assigned_agents:
            result = agent.execute(request.company, request.question)
            agent_results.append(result)
            
        # 3. Aggregate
        final_report = aggregator.synthesize(agent_results)
        return final_report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.reports.report_builder import ReportBuilder

report_builder_instance = ReportBuilder()

class GenerateReportRequest(BaseModel):
    company: str

@router.post("/generate-report")
async def generate_company_report(request: GenerateReportRequest):
    """
    Enterprise Delivery Endpoint.
    Orchestrates all 6 agents, synthesizes insights, and exports to Markdown/PDF.
    """
    try:
        result = report_builder_instance.generate_report(request.company)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.evaluation.dashboard import generate_dashboard_html
import sqlite3
from app.evaluation.db import DB_PATH
from fastapi.responses import HTMLResponse

@router.get("/metrics")
async def get_raw_metrics():
    """
    Returns raw JSON telemetry for external LLMOps platforms (Datadog, etc.)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_telemetry ORDER BY id DESC LIMIT 50")
    telemetry = cursor.fetchall()
    
    cursor.execute("SELECT * FROM evaluation_metrics ORDER BY id DESC LIMIT 50")
    evals = cursor.fetchall()
    conn.close()
    
    return {"telemetry": telemetry, "evaluations": evals}

@router.get("/evaluation-report", response_class=HTMLResponse)
async def view_dashboard():
    """
    Renders the beautiful HTML LLMOps Dashboard directly in the browser!
    """
    return generate_dashboard_html()

@router.get("/health")
async def health_check():
    """
    Basic ping
    """
    return {"status": "AI System Operational", "version": "1.0.0"}

from app.services.company_analyzer import analyze_company

class CompanyAnalyzeRequest(BaseModel):
    company: str

@router.post("/company/analyze")
async def analyze_company_endpoint(request: CompanyAnalyzeRequest):
    """
    Full Company Intelligence Analysis.
    Runs the complete pipeline: Collect → Clean → Embed → Agents → Report.
    """
    try:
        result = await analyze_company(request.company)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

