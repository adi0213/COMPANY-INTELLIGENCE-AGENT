"""
Coordinator Agent Module

Why we need this:
- The Coordinator is the Semantic Router.
- Instead of forcing the LLM to process every single document, the Coordinator 
  reads the user's question and decides WHICH specialized agents need to run.

Architecture & Design Decisions:
- In production, you can use an LLM for routing (e.g., "Given this question, return JSON of which agents to use").
  However, this adds 2-5 seconds of latency before any real work begins!
- We use a "Rule-based Semantic Router". It matches keywords and intents in Python, 
  which is 0 latency, 100% deterministic, and costs $0.
"""

import logging
from typing import List

from app.agents.base_agent import BaseAgent
from app.agents.company_agent import CompanyAgent
from app.agents.news_agent import NewsAgent
from app.agents.hiring_agent import HiringAgent
from app.agents.salary_agent import SalaryAgent
from app.agents.tech_agent import TechAgent
from app.agents.interview_agent import InterviewAgent

logger = logging.getLogger(__name__)

class CoordinatorAgent:
    def __init__(self):
        """
        Initializes the roster of available agents and their semantic triggers.
        """
        # Instantiate the team
        self.company_agent = CompanyAgent()
        self.news_agent = NewsAgent()
        self.hiring_agent = HiringAgent()
        self.salary_agent = SalaryAgent()
        self.tech_agent = TechAgent()
        self.interview_agent = InterviewAgent()
        
        # Define semantic triggers (keyword mappings)
        self.routes = {
            "company": (self.company_agent, ["overview", "history", "who is", "founder", "business model", "what does", "company"]),
            "news": (self.news_agent, ["news", "recently", "announced", "launch", "latest", "press", "event"]),
            "hiring": (self.hiring_agent, ["hiring", "jobs", "roles", "openings", "careers", "recruit", "remote"]),
            "salary": (self.salary_agent, ["salary", "pay", "compensation", "bonus", "equity", "rsu", "benefits", "stock"]),
            "tech": (self.tech_agent, ["tech stack", "programming", "language", "cloud", "aws", "gcp", "ai", "artificial intelligence", "framework", "technology"]),
            "interview": (self.interview_agent, ["interview", "leetcode", "process", "behavioral", "round", "prepare", "questions"])
        }
        logger.info("Coordinator Agent online. Team roster loaded.")

    def route_query(self, question: str) -> List[BaseAgent]:
        """
        Analyzes the question and returns a list of agents that should handle it.
        """
        logger.info(f"[Coordinator] Analyzing query: '{question}'")
        
        selected_agents = set()
        question_lower = question.lower()
        
        for route_name, (agent_instance, keywords) in self.routes.items():
            for kw in keywords:
                if kw in question_lower:
                    selected_agents.add(agent_instance)
                    logger.info(f"[Coordinator] Routing to {agent_instance.name} (Matched keyword: '{kw}')")
                    break # Stop checking keywords for this agent if it already matched
        
        # Fallback: If no specific agent matched, default to the CompanyAgent 
        # so we at least try to provide a general overview.
        if not selected_agents:
            logger.warning("[Coordinator] No specific intent matched. Defaulting to CompanyOverviewAgent.")
            selected_agents.add(self.company_agent)
            
        return list(selected_agents)
