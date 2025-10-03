"""
Example 02: Qdrant Document Ingestion

This example shows how to:
1. Connect to Qdrant Cloud
2. Create a collection
3. Generate embeddings for documents
4. Ingest documents into Qdrant

Run this example:
    python examples/02_qdrant_ingestion.py
"""

import os
import uuid

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

# Sample documents about AI and course topics
SAMPLE_DOCUMENTS = [
    {
        "content": "OpenAI Agents SDK is a powerful framework for building autonomous AI agents. It provides built-in support for function calling, memory management, and conversation threading.",
        "metadata": {"source": "openai_agents_guide.md", "topic": "agents", "page": 1},
    },
    {
        "content": "RAG (Retrieval-Augmented Generation) combines information retrieval with language generation. It allows AI systems to access external knowledge bases and provide more accurate, grounded responses.",
        "metadata": {"source": "rag_fundamentals.md", "topic": "rag", "page": 1},
    },
    {
        "content": "Qdrant is a vector database optimized for similarity search. It supports HNSW indexing for fast approximate nearest neighbor search and offers both cloud and self-hosted options.",
        "metadata": {"source": "qdrant_overview.md", "topic": "vector_db", "page": 1},
    },
    {
        "content": "FastAPI is a modern, fast web framework for building APIs with Python. It provides automatic API documentation, request validation, and async support out of the box.",
        "metadata": {"source": "fastapi_intro.md", "topic": "api", "page": 1},
    },
    {
        "content": "Docker containers package applications with their dependencies, ensuring consistent deployment across environments. Docker Compose allows you to define multi-container applications.",
        "metadata": {"source": "docker_basics.md", "topic": "deployment", "page": 1},
    },
    {
        "content": "Production AI systems require monitoring, error handling, and scalability. Key considerations include API rate limiting, caching, and graceful degradation.",
        "metadata": {"source": "production_ai.md", "topic": "production", "page": 1},
    },
]


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


def main():
    """Run the document ingestion example."""
    print("📚 Qdrant Document Ingestion Example")
    print("=" * 50)

    # Initialize clients
    print("\n1️⃣ Initializing clients...")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "course_documents")

    # Create collection
    print(f"\n2️⃣ Creating collection '{collection_name}'...")
    try:
        qdrant_client.delete_collection(collection_name)
        print(f"   Deleted existing collection")
    except Exception:
        pass

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=1536,  # text-embedding-3-small dimension
            distance=Distance.COSINE,
        ),
    )
    print(f"   ✅ Collection created successfully")

    # Ingest documents
    print(f"\n3️⃣ Ingesting {len(SAMPLE_DOCUMENTS)} documents...")
    points = []

    for i, doc in enumerate(SAMPLE_DOCUMENTS, 1):
        print(f"   Processing document {i}/{len(SAMPLE_DOCUMENTS)}...")

        # Generate embedding
        embedding = generate_embedding(doc["content"], openai_client)

        # Create point
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"content": doc["content"], **doc["metadata"]},
        )
        points.append(point)

    # Upload to Qdrant
    qdrant_client.upsert(collection_name=collection_name, points=points)

    print(f"   ✅ Ingested {len(points)} documents")

    # Verify ingestion
    print(f"\n4️⃣ Verifying ingestion...")
    collection_info = qdrant_client.get_collection(collection_name)
    print(f"   Collection size: {collection_info.points_count} points")
    print(f"   Vector dimension: {collection_info.config.params.vectors.size}")

    print("\n✅ Ingestion complete!")
    print("\n💡 Key Takeaways:")
    print("   - Qdrant stores vectors with associated metadata")
    print("   - Each document is converted to an embedding vector")
    print("   - Collections can be configured with different distance metrics")
    print("   - Metadata enables filtering and context in results")


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
