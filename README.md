# 🏢 Company Intelligence Agent

![Build Status](https://img.shields.io/badge/build-passing-success?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

An autonomous AI research pipeline and brutalist web dashboard that synthesizes deep organizational intelligence. Give it a company name, and the agent scrapes the web, processes the data through a custom RAG (Retrieval-Augmented Generation) pipeline, and outputs highly accurate, structured intelligence reports.

## 🚀 Features

- **Autonomous Data Ingestion:** Automatically crawls company pages, news feeds, and professional networks using Firecrawl and Hunter.io.
- **Advanced RAG Pipeline:** Data is cleaned, chunked, tokenized, embedded, and stored in a local ChromaDB vector database.
- **LLM Synthesis:** Multi-agent evaluation (powered by Google Gemini) synthesizes accurate reports covering:
  - 🏢 Executive Overviews
  - ⚙️ Key Technologies & Tech Stack
  - 💼 Hiring Trends & Interview Focus Areas
  - 💰 Salary Insights
- **Developer Assessment Suite:** Generates dynamic aptitude tests, coding evaluations, and personalized learning roadmaps based on a target company's exact interview style.
- **Brutalist UI Dashboard:** A fully responsive, highly customized React/Vite frontend featuring an animated, S-Curve data flow architecture visualizer.

---

## 📸 Showcase

*(Add your screenshots to the `docs/` folder in your repository to display them here!)*

### Intelligence Dashboard
> **[Insert Screenshot Here]**
> `![Intelligence Dashboard](docs/dashboard.png)`
*The main intelligence view, displaying real-time AI confidence scores and structured company data.*

### System Architecture
> **[Insert Screenshot Here]**
> `![Architecture Flow](docs/architecture.png)`
*The animated S-Curve pipeline visualizing the flow of data from raw internet ingestion to vector database embeddings.*

### Assessment Agent
> **[Insert Screenshot Here]**
> `![Assessment Tool](docs/assessment.png)`
*Dynamic aptitude and coding evaluations tailored to the specific company's hiring profile.*

---

## 🏗️ System Architecture

The system is split into two specialized layers:

1. **The Python Backend (FastAPI)**
   - **Ingestion:** API collectors gather raw HTML, XML, and JSON.
   - **Vector DB:** ChromaDB manages embeddings for semantic search.
   - **Agents:** Orchestrates the multi-agent generative pipeline to cross-verify facts and prevent hallucinations.
2. **The React Frontend (Vite + TypeScript)**
   - Custom Brutalist design system.
   - State management via Zustand.
   - React Flow for pipeline visualization.

---

## 💻 Local Development

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/adi0213/COMPANY-INTELLIGENCE-AGENT.git
cd COMPANY-INTELLIGENCE-AGENT

# Create a virtual environment and install dependencies
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

## 🔑 Environment Variables
You will need a `.env` file in the root directory with the following keys to enable the scraping and AI agents:
```env
GEMINI_API_KEY=your_key_here
FIRECRAWL_API_KEY=your_key_here
HUNTER_API_KEY=your_key_here
WEBSHARE_PROXY=your_proxy_here
```

## 🌍 Deployment
- **Backend:** Deployed on Render (`https://company-intelligence-agent-6hca.onrender.com`)
- **Frontend:** Deployed on Netlify with CI/CD hooked to the `COMPANY-INTELLIGENCE-AGENT-WEB` repository.

---
**© 2026 Developed by [Adith S](https://github.com/adi0213)**
