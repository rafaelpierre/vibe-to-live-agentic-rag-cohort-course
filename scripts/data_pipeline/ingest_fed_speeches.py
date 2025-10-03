#!/usr/bin/env python3
"""
Fed Speeches Ingestion Script for Qdrant with FastEmbed

This script ingests Federal Reserve speeches from JSONL files into Qdrant 
using FastEmbed for vector embeddings.
"""

import json
import os
from typing import List, Dict, Any
from pathlib import Path

from qdrant_client import QdrantClient, models


def load_fed_speeches(data_path: str) -> List[Dict[str, Any]]:
    """Load Federal Reserve speeches from JSONL file."""
    speeches = []
    
    # Load the JSONL file
    jsonl_path = Path(data_path) / "fed_speeches" / "speeches.jsonl"
    
    if not jsonl_path.exists():
        raise FileNotFoundError(f"Speeches file not found at {jsonl_path}")
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            speech = json.loads(line.strip())
            speeches.append(speech)
    
    print(f"Loaded {len(speeches)} speeches from {jsonl_path}")
    return speeches


def setup_qdrant_client() -> QdrantClient:
    """Initialize Qdrant client with cloud configuration."""
    # Get API key from environment variables
    api_key = os.getenv("QDRANT_API_KEY")
    if not api_key:
        raise ValueError("QDRANT_API_KEY environment variable not set")
    
    # You'll need to replace this URL with your actual Qdrant cloud URL
    qdrant_url = os.getenv("QDRANT_URL", "https://your-cluster.qdrant.io")
    
    client = QdrantClient(
        url=qdrant_url,
        api_key=api_key,
    )
    
    return client


def create_collection(client: QdrantClient, collection_name: str, model_name: str) -> None:
    """Create a Qdrant collection with appropriate vector configuration."""
    try:
        # Check if collection already exists
        collections = client.get_collections().collections
        if any(collection.name == collection_name for collection in collections):
            print(f"Collection '{collection_name}' already exists")
            return
        
        # Create collection with vector configuration based on the embedding model
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=client.get_embedding_size(model_name),
                distance=models.Distance.COSINE
            ),
        )
        print(f"Created collection '{collection_name}' with model '{model_name}'")
        
    except Exception as e:
        print(f"Error creating collection: {e}")
        raise


def prepare_documents_for_ingestion(speeches: List[Dict[str, Any]]) -> tuple:
    """Prepare speeches data for Qdrant ingestion."""
    docs = []
    metadata = []
    ids = []
    
    for i, speech in enumerate(speeches):
        # Use the speech content as the document text
        doc_text = speech.get("content", "")
        
        # Skip if no content
        if not doc_text.strip():
            continue
        
        docs.append(doc_text)
        
        # Prepare metadata (excluding the content to avoid duplication)
        meta = {
            "title": speech.get("title", ""),
            "url": speech.get("url", ""),
            "author": speech.get("author", ""),
            "subject": speech.get("subject", ""),
            "description": speech.get("description", ""),
            "category": speech.get("category", ""),
            "pub_date": speech.get("pub_date", ""),
            "content_length": speech.get("content_length", 0),
            "scraped_at": speech.get("scraped_at", ""),
            "document": doc_text  # Include full document text in metadata for retrieval
        }
        metadata.append(meta)
        
        # Use incremental IDs starting from 1
        ids.append(i + 1)
    
    print(f"Prepared {len(docs)} documents for ingestion")
    return docs, metadata, ids


def ingest_speeches_to_qdrant(
    client: QdrantClient,
    collection_name: str,
    docs: List[str],
    metadata: List[Dict[str, Any]],
    ids: List[int],
    model_name: str
) -> None:
    """Ingest prepared speeches into Qdrant collection."""
    try:
        # Upload documents using FastEmbed integration
        client.upload_collection(
            collection_name=collection_name,
            vectors=[models.Document(text=doc, model=model_name) for doc in docs],
            payload=metadata,
            ids=ids,
        )
        print(f"Successfully ingested {len(docs)} documents into '{collection_name}'")
        
    except Exception as e:
        print(f"Error ingesting documents: {e}")
        raise


def verify_ingestion(client: QdrantClient, collection_name: str) -> None:
    """Verify that documents were successfully ingested."""
    try:
        collection_info = client.get_collection(collection_name)
        point_count = collection_info.points_count
        print(f"Collection '{collection_name}' now contains {point_count} points")
        
        # Perform a sample search to verify functionality
        search_results = client.search(
            collection_name=collection_name,
            query_text="monetary policy",
            limit=3
        )
        
        print(f"Sample search returned {len(search_results)} results")
        if search_results:
            print(f"Top result score: {search_results[0].score:.4f}")
            print(f"Top result title: {search_results[0].payload.get('title', 'N/A')}")
        
    except Exception as e:
        print(f"Error verifying ingestion: {e}")
        raise


def main():
    """Main ingestion pipeline."""
    # Configuration
    DATA_PATH = "/Users/rafaelpierre/projects/vibe-to-live-agentic-rag-cohort-course/data"
    COLLECTION_NAME = "fed_speeches"
    MODEL_NAME = "BAAI/bge-small-en"
    
    try:
        print("Starting Fed Speeches ingestion pipeline...")
        
        # Step 1: Load speeches data
        print("\n1. Loading Fed speeches data...")
        speeches = load_fed_speeches(DATA_PATH)
        
        # Step 2: Setup Qdrant client
        print("\n2. Setting up Qdrant client...")
        client = setup_qdrant_client()
        
        # Step 3: Create collection
        print("\n3. Creating Qdrant collection...")
        create_collection(client, COLLECTION_NAME, MODEL_NAME)
        
        # Step 4: Prepare documents
        print("\n4. Preparing documents for ingestion...")
        docs, metadata, ids = prepare_documents_for_ingestion(speeches)
        
        # Step 5: Ingest documents
        print("\n5. Ingesting documents into Qdrant...")
        ingest_speeches_to_qdrant(client, COLLECTION_NAME, docs, metadata, ids, MODEL_NAME)
        
        # Step 6: Verify ingestion
        print("\n6. Verifying ingestion...")
        verify_ingestion(client, COLLECTION_NAME)
        
        print("\n✅ Fed Speeches ingestion completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        raise


if __name__ == "__main__":
    main()
