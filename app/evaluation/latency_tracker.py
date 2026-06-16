"""
Latency Tracker

Why we need this:
- Enterprise SLAs require strict latency boundaries. 
- We use a Python decorator to automatically time any function in our pipeline.
"""

import time
import logging
from functools import wraps
from app.evaluation.db import log_telemetry

logger = logging.getLogger(__name__)

def track_latency(endpoint_name: str):
    """
    Decorator that tracks how long a function takes and logs it to SQLite.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            latency_ms = (end_time - start_time) * 1000.0
            logger.info(f"[{endpoint_name}] Execution time: {latency_ms:.2f}ms")
            
            # Extract company name if it's passed as an argument (hacky but works for our pipeline)
            company = kwargs.get('company_name', 'Unknown')
            if 'company_name' not in kwargs and len(args) > 0 and isinstance(args[0], str):
                company = args[0]
                
            # Log to DB (assume 0 tokens and $0 cost for generic latency tracking)
            log_telemetry(company, endpoint_name, latency_ms, 0, 0.0)
            
            return result
        return wrapper
    return decorator
