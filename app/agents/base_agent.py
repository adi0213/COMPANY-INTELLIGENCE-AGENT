"""
Base Agent Module

Why we need this:
- Object-Oriented Design (OOD): All specialized agents share common functionality
  (e.g., they all need to execute RAG, they all need an LLM). 
- We define a single `BaseAgent` class that implements the core execution loop.
  Specialized agents will inherit from this and just provide their own unique Prompts
  and specific Metadata Filters.
"""

import logging
from typing import Dict, Any
from abc import ABC, abstractmethod

from app.services.rag_service import execute_rag_pipeline

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str, role_description: str):
        """
        Initializes the agent with its persona.
        """
        self.name = name
        self.role_description = role_description
        logger.info(f"Initialized Agent: {self.name} - Role: {self.role_description}")

    @abstractmethod
    def get_domain_filter(self) -> str:
        """
        Returns the specific domain keyword this agent searches for.
        E.g., "tech_stack", "jobs", "news".
        Must be implemented by child classes.
        """
        pass

    def execute(self, company_name: str, question: str) -> Dict[str, Any]:
        """
        The core tool execution loop for an agent.
        Instead of answering blindly, the agent uses its "RAG Tool" to fetch
        data specifically filtered to its domain.
        """
        logger.info(f"[{self.name}] Executing task: {question}")
        
        # We modify the question slightly to force the Retriever to focus on this agent's domain
        domain_focused_question = f"Regarding {self.get_domain_filter()}: {question}"
        
        # Execute the RAG pipeline. 
        # In a real framework (like LangChain), this is where the Agent would decide 
        # WHICH tool to call. Since we only have one tool (RAG), it calls it directly.
        result = execute_rag_pipeline(company_name, domain_focused_question)
        
        # We append the agent's name to the result so the Aggregator knows who generated it
        result["agent_name"] = self.name
        
        return result
