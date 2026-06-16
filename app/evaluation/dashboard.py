"""
Dashboard Module

Why we need this:
- Raw SQLite tables are hard to read.
- We serve a beautiful HTML dashboard directly from FastAPI so executives and 
  engineers can visually monitor the health, cost, and hallucination rates of the AI.
"""

import sqlite3
from fastapi.responses import HTMLResponse
from app.evaluation.db import DB_PATH

def generate_dashboard_html() -> HTMLResponse:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get basic stats
    cursor.execute("SELECT COUNT(*), AVG(latency_ms) FROM system_telemetry")
    row = cursor.fetchone()
    total_requests = row[0] or 0
    avg_latency = row[1] or 0.0
    
    cursor.execute("SELECT AVG(hallucination_score) FROM evaluation_metrics")
    row = cursor.fetchone()
    avg_score = row[0] or 1.0 # Default to perfect if no data
    
    conn.close()
    
    # Calculate health metric
    health_status = "Healthy" if avg_score > 0.8 else "Degraded"
    health_color = "green" if health_status == "Healthy" else "red"
    
    html_content = f"""
    <html>
        <head>
            <title>LLMOps Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 40px; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                .container {{ display: flex; justify-content: space-around; margin-top: 50px; }}
                .card {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; width: 25%; }}
                .metric {{ font-size: 40px; font-weight: bold; color: #3498db; margin-top: 10px; }}
                .health {{ font-size: 40px; font-weight: bold; color: {health_color}; margin-top: 10px; }}
            </style>
        </head>
        <body>
            <h1>Enterprise AI Observability Dashboard</h1>
            <div class="container">
                <div class="card">
                    <h3>System Health</h3>
                    <div class="health">{health_status}</div>
                </div>
                <div class="card">
                    <h3>Total Requests</h3>
                    <div class="metric">{total_requests}</div>
                </div>
                <div class="card">
                    <h3>Avg Latency</h3>
                    <div class="metric">{avg_latency:.0f} ms</div>
                </div>
                <div class="card">
                    <h3>Avg Groundedness Score</h3>
                    <div class="metric">{avg_score * 100:.1f}%</div>
                </div>
            </div>
            <p style="text-align: center; margin-top: 50px; color: #7f8c8d;">Data pulled directly from local LLMOps Telemetry SQLite Database.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
