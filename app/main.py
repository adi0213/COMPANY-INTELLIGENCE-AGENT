"""
Main application entry point for the Company Intelligence Agent (Phase 2).

Why we need this:
- Every web application needs a starting point. `main.py` is the bootstrap file for our FastAPI application.
- It initializes the app, configures middleware (like CORS), and registers routers.

Architecture & Design Decisions:
- We use FastAPI because it is extremely fast, asynchronous by default, and auto-generates documentation (Swagger UI).
- We separate routes into a different folder (`api/routes.py`) to keep `main.py` clean. This is a standard industry practice called "Separation of Concerns". If we had all routes in `main.py`, it would become thousands of lines long and unmaintainable.

Future Scalability (Later Phases):
- In later phases (Data Cleaning, Embeddings, LLM Analysis), we will simply register new routers here (e.g., `app.include_router(llm.router)`).
- We can also add global exception handlers and database connection pooling in this file.

Common Mistakes:
- Putting all business logic directly into `main.py` routes. Instead, routes should only handle HTTP logic, delegating the actual work to the `services` layer.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

# Initialize the FastAPI application
# We provide metadata that will appear in the auto-generated /docs endpoint.
app = FastAPI(
    title="Company Intelligence Agent - Data Collection API",
    description="Phase 2: API for orchestrating data collection about companies.",
    version="0.1.0"
)

# Enable CORS so the React frontend can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins since frontend is deployed remotely
    allow_credentials=False, # Must be False if allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes from our API module
# We prefix them with /api/v1 as a best practice for API versioning.
# If we ever make breaking changes, we can create /api/v2 without breaking existing clients.
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Health check endpoint.
    
    Why we need this:
    - Load balancers (like AWS ALB or NGINX) and deployment platforms (like Kubernetes) 
      constantly "ping" this endpoint to check if the server is alive.
    """
    return {"status": "ok", "message": "Company Intelligence Agent API is running."}

# To run this file locally, use:
# uvicorn app.main:app --reload
