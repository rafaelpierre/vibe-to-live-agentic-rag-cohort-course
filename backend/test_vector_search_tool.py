#!/usr/bin/env python3
"""
Quick test script for VectorSearchTool
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.vector_search import VectorSearchTool, search_knowledge_base


def main():
    """Test the vector search tool."""
    
    print("🧪 Testing VectorSearchTool\n")
    print("=" * 80)
    
    # Test 1: Initialize tool
    print("\n1️⃣  Initializing VectorSearchTool...")
    try:
        tool = VectorSearchTool()
        print("✅ Tool initialized successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Verify collection
    print("\n2️⃣  Verifying collection...")
    collection_info = tool.verify_collection()
    if collection_info["exists"]:
        print(f"✅ Collection '{tool.collection_name}' exists")
        print(f"   Points: {collection_info['points_count']}")
        print(f"   Vector size: {collection_info['vector_size']}")
    else:
        print(f"❌ Collection not found: {collection_info.get('error')}")
        print("   Run scripts/data_pipeline/ingest_fed_speeches.py first")
        return
    
    # Test 3: Perform search
    print("\n3️⃣  Performing search...")
    query = "monetary policy and interest rates"
    print(f"   Query: '{query}'")
    
    try:
        results = tool.search(query, limit=3)
        print(f"✅ Search returned {len(results)} results\n")
        
        for idx, result in enumerate(results, 1):
            print(f"📊 Result {idx}:")
            print(f"   Score: {result['score']:.4f}")
            print(f"   Title: {result['metadata']['title']}")
            print(f"   Speaker: {result['metadata']['speaker']}")
            print(f"   Date: {result['metadata']['pub_date']}")
            print()
    except Exception as e:
        print(f"❌ Search error: {e}")
        return
    
    # Test 4: Test the tool function
    print("\n4️⃣  Testing search_knowledge_base function...")
    try:
        output = search_knowledge_base("inflation and economic growth", limit=2)
        print("✅ Function executed successfully\n")
        print("Output:")
        print(output)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("✅ All tests completed!")


if __name__ == "__main__":
    main()
