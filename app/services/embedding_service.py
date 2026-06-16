"""
Embedding Service

Why we need this:
- Orchestrates Phase 4 and Phase 5.
- It takes a cleaned dictionary, extracts the useful text (descriptions, news summaries),
  chunks them, embeds them, attaches metadata, and writes them to the Vector DB.
"""

import logging
from typing import Dict, Any, List

from app.embeddings.chunker import TextChunker
from app.embeddings.embedder import Embedder
from app.embeddings.metadata import create_metadata, generate_chunk_id
from app.vector_db.indexer import index_chunks

logger = logging.getLogger(__name__)

# Initialize globally to avoid reloading model on every request
chunker = TextChunker()
embedder = Embedder()

def process_and_index_company(clean_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Chunks, embeds, and indexes cleaned data into ChromaDB.
    """
    company_name = clean_data.get("company", {}).get("name", "Unknown")
    logger.info(f"Starting embedding pipeline for {company_name}")
    
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    # 1. Process Company Description & Key Details
    comp = clean_data.get("company", {})
    desc = comp.get("description", "")
    metadata_fields = []
    for field in ["industry", "headquarters", "founded", "employees", "website"]:
        val = comp.get(field, "")
        if val:
            metadata_fields.append(f"{field.title()}: {val}")
    
    full_overview_text = desc
    if metadata_fields:
        full_overview_text += "\n\nKey Details:\n" + "\n".join(metadata_fields)
        
    if full_overview_text:
        desc_chunks = chunker.split_text(full_overview_text)
        for i, chunk in enumerate(desc_chunks):
            all_chunks.append(chunk)
            all_metadatas.append(create_metadata(company_name, "overview"))
            all_ids.append(generate_chunk_id(company_name, "overview", i, chunk))
            
    # 2. Process News Articles
    for news_idx, article in enumerate(clean_data.get("news", [])):
        title = article.get("title", "")
        if title:
            # For short news, we might just use the title as the chunk
            all_chunks.append(title)
            all_metadatas.append(create_metadata(company_name, "news", date=article.get("date", "")))
            all_ids.append(generate_chunk_id(company_name, f"news_{news_idx}", 0, title))
            
    # 3. Process Jobs
    for job_idx, role in enumerate(clean_data.get("jobs", {}).get("open_roles", [])):
        if role:
            all_chunks.append(role)
            all_metadatas.append(create_metadata(company_name, "jobs"))
            all_ids.append(generate_chunk_id(company_name, "jobs", job_idx, role))

    # 4. Process Products & Services
    products_info = clean_data.get("products", {})
    for prod_idx, prod in enumerate(products_info.get("products", [])):
        if prod:
            prod_text = f"Product: {prod}"
            all_chunks.append(prod_text)
            all_metadatas.append(create_metadata(company_name, "products"))
            all_ids.append(generate_chunk_id(company_name, "products", prod_idx, prod_text))
            
    for serv_idx, serv in enumerate(products_info.get("services", [])):
        if serv:
            serv_text = f"Service: {serv}"
            all_chunks.append(serv_text)
            all_metadatas.append(create_metadata(company_name, "products"))
            all_ids.append(generate_chunk_id(company_name, "products_serv", serv_idx, serv_text))

    # 5. Process Salary Statistics
    salary_info = clean_data.get("salary", {})
    for role_name, salary_range in salary_info.items():
        if salary_range:
            salary_text = f"{role_name.replace('_', ' ').title()} salary range: {salary_range}"
            all_chunks.append(salary_text)
            all_metadatas.append(create_metadata(company_name, "salary"))
            all_ids.append(generate_chunk_id(company_name, "salary", len(all_chunks), salary_text))
            
    if not all_chunks:
        logger.warning(f"No text to embed for {company_name}")
        return {"chunks_processed": 0, "vector_dimension": 0}
        
    # Generate Embeddings (Batch)
    logger.info(f"Generating embeddings for {len(all_chunks)} chunks...")
    embeddings = embedder.generate_batch_embeddings(all_chunks)
    
    # Index in Vector DB
    index_chunks(all_chunks, embeddings, all_metadatas, all_ids)
    
    return {
        "chunks_processed": len(all_chunks),
        "vector_dimension": len(embeddings[0]) if embeddings else 0
    }
