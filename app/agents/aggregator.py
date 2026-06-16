"""
Aggregator Agent Module

Why we need this:
- The Coordinator might invoke 3 different agents at the same time. 
- Example: "What is Google's AI tech stack and what do they pay AI engineers?"
  -> Routes to: TechAgent AND SalaryAgent.
- The Aggregator takes the output from both agents and stitches them together 
  into a single cohesive response for the user.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AggregatorAgent:
    def __init__(self):
        logger.info("Aggregator Agent online.")
        
    def synthesize(self, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combines multiple agent responses.
        """
        logger.info(f"[Aggregator] Synthesizing reports from {len(agent_results)} agents...")
        
        if not agent_results:
            return {"answer": "No agents were able to process this request.", "sources": []}
            
        if len(agent_results) == 1:
            # If only one agent ran, just return its result directly
            return agent_results[0]
            
        # If multiple agents ran, combine their outputs cleanly
        combined_answer = ""
        combined_sources = []
        
        for result in agent_results:
            agent_name = result.get("agent_name", "UnknownAgent")
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            
            combined_answer += f"### From {agent_name}:\n{answer}\n\n"
            combined_sources.extend(sources)
            
        logger.info("[Aggregator] Synthesis complete.")
        return {
            "answer": combined_answer.strip(),
            "sources": combined_sources
        }
