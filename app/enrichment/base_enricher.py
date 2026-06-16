import logging
from typing import Dict, Any
from app.rag.generator import Generator

logger = logging.getLogger(__name__)

class BaseEnricher:
    """
    Base class for all Data Enrichment modules.
    Provides a shared LLM Generator to synthesize missing data.
    """
    def __init__(self):
        self.generator = Generator()
        
    def enrich(self, company_name: str, clean_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes the cleaned data payload and returns a dictionary of enriched fields.
        """
        raise NotImplementedError("Subclasses must implement enrich()")
