#!/usr/bin/env python3
"""
Fed Speeches Ingestion Script for Qdrant with FastEmbed

This script ingests Federal Reserve speeches from JSONL files into Qdrant Cloud
using FastEmbed for vector embeddings.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

from qdrant_client import QdrantClient, models


def load_speeches_from_jsonl(data_path: Path) -> List[Dict[str, Any]]:
    """Load speeches from JSONL file."""
    jsonl_path = data_path / "fed_speeches" / "speeches.jsonl"
    
    if not jsonl_path.exists():
        raise FileNotFoundError(f"Speeches file not found at {jsonl_path}")
    
    speeches = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            speech = json.loads(line.strip())
            speeches.append(speech)
    
    print(f"✅ Loaded {len(speeches)} speeches from {jsonl_path}")
    return speeches


def main():
    """Main ingestion pipeline."""
    
    # Configuration
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    DATA_PATH = project_root / "data"
    COLLECTION_NAME = "fed_speeches"
    MODEL_NAME = "BAAI/bge-small-en"
    
    # Get Qdrant credentials from environment variables
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    
    if not QDRANT_URL or not QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set")
    
    print("🚀 Starting Fed Speeches ingestion pipeline...\n")
    
    # Step 1: Load speeches from JSONL
    print("1️⃣  Loading speeches from JSONL file...")
    speeches = load_speeches_from_jsonl(DATA_PATH)
    
    # Step 2: Initialize Qdrant client
    print("\n2️⃣  Connecting to Qdrant Cloud...")
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    print("✅ Connected to Qdrant Cloud")
    
    # Step 3: Prepare documents and payload
    print("\n3️⃣  Preparing documents for embedding...")
    payload = []
    docs = []
    ids = []
    
    for i, speech in enumerate(speeches):
        # Extract the document text (the content of the speech)
        doc_text = speech.get("content", "")
        
        # Skip if no content
        if not doc_text.strip():
            continue
        
        # Create Document object with model specified
        docs.append(models.Document(text=doc_text, model=MODEL_NAME))
        
        # Create payload with metadata
        payload.append({
            "title": speech.get("title", ""),
            "speaker": speech.get("author", ""),  # Fixed: field is "author" in JSONL, not "speaker"
            "url": speech.get("url", ""),
            "description": speech.get("description", ""),
            "category": speech.get("category", ""),
            "pub_date": speech.get("pub_date", ""),
            "content_length": speech.get("content_length", 0),
            "scraped_at": speech.get("scraped_at", ""),
            "document": doc_text  # Include full text for retrieval
        })
        
        # Use incremental IDs starting from 1
        ids.append(i + 1)
    
    print(f"✅ Prepared {len(docs)} documents for ingestion")
    
    # Step 4: Create collection
    print("\n4️⃣  Creating Qdrant collection...")
    
    # Delete collection if it exists (for clean re-ingestion)
    try:
        collections = client.get_collections().collections
        if any(collection.name == COLLECTION_NAME for collection in collections):
            print(f"⚠️  Collection '{COLLECTION_NAME}' exists, deleting...")
            client.delete_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"Note: {e}")
    
    # Create new collection
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=client.get_embedding_size(MODEL_NAME),
            distance=models.Distance.COSINE
        )
    )
    print(f"✅ Created collection '{COLLECTION_NAME}' with model '{MODEL_NAME}'")
    
    # Step 5: Upload documents to Qdrant (this will automatically embed using FastEmbed)
    print("\n5️⃣  Uploading documents to Qdrant (embedding with FastEmbed)...")
    client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors=docs,
        payload=payload,
        ids=ids,
    )
    print(f"✅ Successfully uploaded {len(docs)} documents to '{COLLECTION_NAME}'")
    
    # Step 6: Verify ingestion with a test search
    print("\n6️⃣  Verifying ingestion with test search...")
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"✅ Collection now contains {collection_info.points_count} points")
    
    # Perform a sample search
    search_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=models.Document(text="monetary policy and interest rates", model=MODEL_NAME),
        limit=3
    ).points
    
    print(f"✅ Sample search returned {len(search_results)} results")
    if search_results:
        print(f"\n📊 Top result:")
        print(f"   Score: {search_results[0].score:.4f}")
        print(f"   Title: {search_results[0].payload.get('title', 'N/A')}")
        print(f"   Speaker: {search_results[0].payload.get('speaker', 'N/A')}")
    
    print("\n✨ Fed Speeches ingestion completed successfully!")


if __name__ == "__main__":
    main()