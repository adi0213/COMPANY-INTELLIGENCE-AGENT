"""
Report Builder

Orchestrates the Specialized Agents, triggers the LLM Synthesis engines, 
and exports the final structured document.
"""

import logging
from typing import Dict, Any

from app.agents.coordinator import CoordinatorAgent
from app.reports.report_templates import get_base_template
from app.reports.executive_summary import ExecutiveSummaryGenerator
from app.reports.risk_analysis import RiskAnalysisGenerator
from app.reports.opportunity_analysis import OpportunityAnalysisGenerator
from app.reports.markdown_exporter import MarkdownExporter
from app.reports.pdf_exporter import PDFExporter

logger = logging.getLogger(__name__)

class ReportBuilder:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.exec_gen = ExecutiveSummaryGenerator()
        self.risk_gen = RiskAnalysisGenerator()
        self.opp_gen = OpportunityAnalysisGenerator()
        self.md_export = MarkdownExporter()
        self.pdf_export = PDFExporter()

    def generate_report(self, company_name: str) -> Dict[str, Any]:
        logger.info(f"Initiating full report build for {company_name}")
        
        # 1. Wake up all specific agents manually or via coordinator (we'll just use the agents directly for standard sections)
        sections = {}
        
        # Parallelization or async would be ideal here, but sequential is easier for debugging
        logger.info("[ReportBuilder] Fetching Company Overview...")
        sections["company_overview"] = self.coordinator.company_agent.execute(company_name, "What is the company overview and history?")["answer"]
        
        logger.info("[ReportBuilder] Fetching Tech Stack...")
        sections["tech"] = self.coordinator.tech_agent.execute(company_name, "What is the tech stack?")["answer"]
        
        logger.info("[ReportBuilder] Fetching Hiring Trends...")
        sections["hiring"] = self.coordinator.hiring_agent.execute(company_name, "What are the hiring trends?")["answer"]
        
        logger.info("[ReportBuilder] Fetching Salary Insights...")
        sections["salary"] = self.coordinator.salary_agent.execute(company_name, "What are the salary and compensation details?")["answer"]
        
        logger.info("[ReportBuilder] Fetching Products & Services...")
        # Since we didn't explicitly make a product agent, we use company agent for products too
        sections["products"] = self.coordinator.company_agent.execute(company_name, "What are their main products and services?")["answer"]
        
        logger.info("[ReportBuilder] Fetching News...")
        sections["news"] = self.coordinator.news_agent.execute(company_name, "What are the recent news and developments?")["answer"]
        
        logger.info("[ReportBuilder] Fetching Interview Prep...")
        sections["interview"] = self.coordinator.interview_agent.execute(company_name, "What is the interview process and focus?")["answer"]
        
        # 2. Combine into an initial draft
        raw_draft = ""
        for key, text in sections.items():
            raw_draft += f"[{key.upper()}]\n{text}\n\n"
            
        # 3. LLM Synthesis (Exec Summary, Risks, Opportunities)
        logger.info("[ReportBuilder] Running LLM Synthesis on full draft...")
        sections["executive_summary"] = self.exec_gen.generate(raw_draft)
        sections["risks"] = self.risk_gen.generate(raw_draft)
        sections["opportunities"] = self.opp_gen.generate(raw_draft)
        
        # 4. Format into final Template
        final_md = get_base_template(company_name).format(**sections)
        
        # 5. Export
        md_path = self.md_export.export(company_name, final_md)
        pdf_path = self.pdf_export.export(company_name, final_md)
        
        return {
            "status": "Success",
            "company": company_name,
            "markdown_path": md_path,
            "pdf_path": pdf_path,
            "report_content": final_md
        }
