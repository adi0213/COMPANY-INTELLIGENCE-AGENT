"""
Evaluation Database — Lightweight Telemetry Store

Uses a single persistent SQLite connection to avoid opening/closing
connections on every agent call (which wastes file handles).
"""

import os
import sqlite3
import logging
import threading

logger = logging.getLogger(__name__)

DB_PATH = "data/metrics.db"

# Thread-safe singleton connection
_local = threading.local()


def _get_conn():
    """Returns a thread-local SQLite connection (reused across calls)."""
    if not hasattr(_local, "conn") or _local.conn is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        _local.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _local.conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        _init_tables(_local.conn)
    return _local.conn


def _init_tables(conn):
    """Creates tables if they don't exist."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            company TEXT,
            endpoint TEXT,
            latency_ms REAL,
            token_count INTEGER,
            estimated_cost REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluation_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            question TEXT,
            agent_name TEXT,
            retrieved_chunks INTEGER,
            hallucination_score REAL,
            faithfulness_score REAL
        )
    ''')
    conn.commit()
    logger.info("Metrics Database initialized successfully.")


def init_db():
    """Public init — just ensures connection and tables exist."""
    _get_conn()


def log_telemetry(company: str, endpoint: str, latency_ms: float, token_count: int, estimated_cost: float):
    try:
        conn = _get_conn()
        conn.execute(
            'INSERT INTO system_telemetry (company, endpoint, latency_ms, token_count, estimated_cost) VALUES (?, ?, ?, ?, ?)',
            (company, endpoint, latency_ms, token_count, estimated_cost),
        )
        conn.commit()
    except Exception as e:
        logger.warning(f"Failed to log telemetry: {e}")


def log_evaluation(question: str, agent_name: str, retrieved_chunks: int, hallucination_score: float, faithfulness_score: float):
    try:
        conn = _get_conn()
        conn.execute(
            'INSERT INTO evaluation_metrics (question, agent_name, retrieved_chunks, hallucination_score, faithfulness_score) VALUES (?, ?, ?, ?, ?)',
            (question, agent_name, retrieved_chunks, hallucination_score, faithfulness_score),
        )
        conn.commit()
    except Exception as e:
        logger.warning(f"Failed to log evaluation: {e}")


# Initialize upon import
init_db()
