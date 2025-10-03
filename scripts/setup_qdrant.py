"""
Setup script to populate Qdrant Cloud with sample course documents.

This script:
1. Loads sample documents from data/sample_docs/
2. Generates embeddings using OpenAI
3. Creates a Qdrant collection
4. Uploads documents to Qdrant

Run this script:
    cd backend && uv run python ../scripts/setup_qdrant.py
"""

import os
import sys
import uuid
from pathlib import Path

# Add backend/src to Python path
backend_src = Path(__file__).parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_src))

try:
    from openai import OpenAI
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams
except ImportError:
    print("❌ Error: Required packages not found.")
    print("Please run: cd backend && uv sync")
    sys.exit(1)


def load_documents(docs_dir: Path) -> list[dict]:
    """
    Load documents from the sample_docs directory.

    Args:
        docs_dir: Path to sample_docs directory

    Returns:
        List of document dictionaries
    """
    documents = []

    for file_path in docs_dir.glob("*.md"):
        with open(file_path, "r") as f:
            content = f.read()

        # Extract topic from filename
        topic = file_path.stem.replace("_", " ")

        documents.append(
            {
                "content": content,
                "metadata": {
                    "source": file_path.name,
                    "topic": topic,
                    "page": 1,
                },
            }
        )

    return documents


def generate_embedding(text: str, client: OpenAI) -> list[float]:
    """Generate embedding for text using OpenAI."""
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def main():
    """Run the setup script."""
    print("🚀 Qdrant Setup Script")
    print("=" * 50)

    # Check environment variables
    required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ Error: Missing environment variables: {', '.join(missing_vars)}")
        print("\nPlease set them in your .env file:")
        print("  OPENAI_API_KEY=your-key-here")
        print("  QDRANT_URL=your-qdrant-url")
        print("  QDRANT_API_KEY=your-qdrant-key")
        sys.exit(1)

    # Initialize clients
    print("\n1️⃣ Initializing clients...")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    print("   ✅ Clients initialized")

    # Load documents
    print("\n2️⃣ Loading sample documents...")
    docs_dir = Path(__file__).parent.parent / "data" / "sample_docs"

    if not docs_dir.exists():
        print(f"❌ Error: Sample docs directory not found: {docs_dir}")
        sys.exit(1)

    documents = load_documents(docs_dir)
    print(f"   ✅ Loaded {len(documents)} documents")

    # Create collection
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "course_documents")
    print(f"\n3️⃣ Setting up collection '{collection_name}'...")

    try:
        qdrant_client.delete_collection(collection_name)
        print("   🗑️  Deleted existing collection")
    except Exception:
        pass

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=1536,  # text-embedding-3-small dimension
            distance=Distance.COSINE,
        ),
    )
    print("   ✅ Collection created")

    # Generate embeddings and upload
    print(f"\n4️⃣ Generating embeddings and uploading...")
    points = []

    for i, doc in enumerate(documents, 1):
        print(f"   Processing {i}/{len(documents)}: {doc['metadata']['source']}")

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
    print(f"   ✅ Uploaded {len(points)} documents")

    # Verify
    print(f"\n5️⃣ Verifying setup...")
    collection_info = qdrant_client.get_collection(collection_name)
    print(f"   Collection: {collection_name}")
    print(f"   Points: {collection_info.points_count}")
    print(f"   Vector size: {collection_info.config.params.vectors.size}")

    print("\n✅ Setup complete!")
    print("\n📝 Next steps:")
    print("   1. Complete the Week 1 assignment in backend/src/")
    print("   2. Test your implementation with: docker-compose up")
    print("   3. Access the API docs at: http://localhost:8000/docs")
    print("   4. Try the examples in the examples/ folder")


if __name__ == "__main__":
    main()
