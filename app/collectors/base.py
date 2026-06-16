"""
Base Collector Interface for the Company Intelligence Agent.

Why we need this:
- We have multiple collectors (Company, News, Jobs, Salary, Products).
- Without a strict interface, developers might implement different method names 
  (e.g., `get_data()`, `fetch()`, `scrape()`), making the aggregator service chaotic and hard to maintain.

Architecture & Design Decisions:
- We use Python's built-in `abc` (Abstract Base Classes) module to define an interface.
- This enforces the "Open/Closed Principle" (from SOLID): Our system is open for extension 
  (you can easily add a 'FinancialsCollector' later) but closed for modification.
- We require an asynchronous `collect` method because network I/O (scraping) is the slowest 
  part of our system. `async` allows us to run all collectors concurrently.

Common Mistakes:
- Skipping interfaces in Python because "it's dynamically typed". As systems grow, lack of 
  strict contracts leads to runtime `AttributeError` exceptions.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseCollector(ABC):
    """
    Abstract Base Class that all data collectors must inherit from.
    """

    @abstractmethod
    async def collect(self, company_name: str) -> Dict[str, Any]:
        """
        Main entry point for collecting data.
        
        Args:
            company_name (str): The target company name.
            
        Returns:
            Dict[str, Any]: A dictionary containing the raw collected data.
                            The schema depends on the specific collector.
        """
        pass
