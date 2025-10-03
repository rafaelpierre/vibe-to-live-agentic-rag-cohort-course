#!/usr/bin/env python3
"""
Example 03: Qdrant Search with FastEmbed

This example demonstrates how to search a Qdrant collection using FastEmbed
for automatic query embedding. It shows:

1. Connecting to Qdrant Cloud
2. Using Document objects with FastEmbed for query embedding
3. Performing semantic search
4. Displaying results with metadata

Prerequisites:
- Qdrant collection 'fed_speeches' must exist (run ingest_fed_speeches.py first)
- QDRANT_URL and QDRANT_API_KEY environment variables must be set
"""

import os
from qdrant_client import QdrantClient, models


def main():
    """Perform semantic search on Fed speeches collection."""
    
    # Configuration
    COLLECTION_NAME = "fed_speeches"
    MODEL_NAME = "BAAI/bge-small-en"
    
    # Get Qdrant credentials from environment variables
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    
    if not QDRANT_URL or not QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set")
    
    print("🚀 Starting Qdrant Search Example...\n")
    
    # Step 1: Initialize Qdrant client
    print("1️⃣  Connecting to Qdrant Cloud...")
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    print("✅ Connected to Qdrant Cloud\n")
    
    # Step 2: Verify collection exists and get info
    print("2️⃣  Checking collection status...")
    try:
        collection_info = client.get_collection(COLLECTION_NAME)
        print(f"✅ Collection '{COLLECTION_NAME}' found")
        print(f"   Points: {collection_info.points_count}")
        print(f"   Vector size: {collection_info.config.params.vectors.size}")
        print(f"   Distance metric: {collection_info.config.params.vectors.distance}\n")
    except Exception as e:
        print(f"❌ Error: Collection '{COLLECTION_NAME}' not found!")
        print(f"   Please run 'scripts/data_pipeline/ingest_fed_speeches.py' first")
        return
    
    # Step 3: Perform semantic search
    print("3️⃣  Performing semantic search...\n")
    
    # Define search query
    query_text = "monetary policy and interest rates"
    print(f"🔍 Query: '{query_text}'\n")
    
    # Perform search using Document object with FastEmbed
    # FastEmbed automatically generates the query embedding
    search_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=models.Document(text=query_text, model=MODEL_NAME),
        limit=3
    ).points
    
    print(f"✅ Sample search returned {len(search_results)} results\n")
    
    # Step 4: Display results
    if search_results:
        print("=" * 80)
        print("📊 SEARCH RESULTS")
        print("=" * 80)
        
        for idx, result in enumerate(search_results, 1):
            print(f"\n🏆 Result #{idx}")
            print(f"{'─' * 80}")
            print(f"Score:       {result.score:.4f}")
            print(f"Title:       {result.payload.get('title', 'N/A')}")
            print(f"Speaker:     {result.payload.get('speaker', 'N/A')}")
            print(f"Date:        {result.payload.get('pub_date', 'N/A')}")
            print(f"Category:    {result.payload.get('category', 'N/A')}")
            print(f"URL:         {result.payload.get('url', 'N/A')}")
            
            # Show a snippet of the content
            content = result.payload.get('document', '')
            if content:
                snippet = content[:200] + "..." if len(content) > 200 else content
                print(f"\nContent Preview:")
                print(f"   {snippet}")
        
        print("\n" + "=" * 80)
        
        # Step 5: Try another search query
        print("\n4️⃣  Trying another search query...\n")
        
        query_text_2 = "inflation and economic growth"
        print(f"🔍 Query: '{query_text_2}'\n")
        
        search_results_2 = client.query_points(
            collection_name=COLLECTION_NAME,
            query=models.Document(text=query_text_2, model=MODEL_NAME),
            limit=3
        ).points
        
        print(f"✅ Search returned {len(search_results_2)} results")
        
        if search_results_2:
            print(f"\n📊 Top result:")
            print(f"   Score: {search_results_2[0].score:.4f}")
            print(f"   Title: {search_results_2[0].payload.get('title', 'N/A')}")
            print(f"   Speaker: {search_results_2[0].payload.get('speaker', 'N/A')}")
    else:
        print("⚠️  No results found")
    
    print("\n✅ Search example completed successfully!")


if __name__ == "__main__":
    main()
