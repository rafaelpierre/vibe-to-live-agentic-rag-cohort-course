"""
Example 03: Qdrant Vector Search

This example shows how to:
1. Connect to Qdrant
2. Generate query embeddings
3. Perform similarity search
4. Interpret and use search results

Run this example:
    python examples/03_qdrant_search.py
"""

import os

from openai import OpenAI
from qdrant_client import QdrantClient


def generate_embedding(text: str, client: OpenAI) -> list[float]:
    """
    Generate an embedding vector for text using OpenAI.

    Args:
        text: Text to embed
        client: OpenAI client instance

    Returns:
        Embedding vector
    """
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def search_documents(
    query: str,
    qdrant_client: QdrantClient,
    openai_client: OpenAI,
    collection_name: str,
    limit: int = 3,
):
    """
    Search for relevant documents using vector similarity.

    Args:
        query: Search query
        qdrant_client: Qdrant client instance
        openai_client: OpenAI client instance
        collection_name: Name of the collection to search
        limit: Maximum number of results

    Returns:
        List of search results
    """
    # Generate query embedding
    query_vector = generate_embedding(query, openai_client)

    # Search Qdrant
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit,
    )

    return results


def main():
    """Run the vector search example."""
    print("🔍 Qdrant Vector Search Example")
    print("=" * 50)

    # Initialize clients
    print("\n1️⃣ Initializing clients...")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "course_documents")

    # Verify collection exists
    try:
        collection_info = qdrant_client.get_collection(collection_name)
        print(
            f"   ✅ Connected to collection '{collection_name}' ({collection_info.points_count} documents)"
        )
    except Exception as e:
        print(f"   ❌ Error: Collection '{collection_name}' not found")
        print(
            "   Please run 02_qdrant_ingestion.py first to create and populate the collection"
        )
        exit(1)

    # Example queries
    queries = [
        "How do I build AI agents?",
        "What is a vector database?",
        "Tell me about deploying applications with containers",
    ]

    print("\n2️⃣ Running search queries...")

    for i, query in enumerate(queries, 1):
        print(f"\n{'=' * 50}")
        print(f"Query {i}: '{query}'")
        print(f"{'=' * 50}")

        results = search_documents(
            query=query,
            qdrant_client=qdrant_client,
            openai_client=openai_client,
            collection_name=collection_name,
            limit=3,
        )

        print(f"\nTop {len(results)} results:")
        for j, result in enumerate(results, 1):
            print(f"\n  Result {j}:")
            print(f"  Score: {result.score:.4f}")
            print(f"  Source: {result.payload.get('source', 'unknown')}")
            print(f"  Topic: {result.payload.get('topic', 'unknown')}")
            print(f"  Content: {result.payload.get('content', '')[:150]}...")

    print("\n✅ Search examples complete!")
    print("\n💡 Key Takeaways:")
    print("   - Vector search finds semantically similar content")
    print("   - Higher scores indicate better matches")
    print("   - Results include both content and metadata")
    print("   - Same query can match different documents based on context")


if __name__ == "__main__":
    # Check for required environment variables
    required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(
            f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}"
        )
        print("Please set them in your .env file")
        exit(1)

    main()
