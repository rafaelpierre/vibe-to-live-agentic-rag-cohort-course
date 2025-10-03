"""
Ingest Federal Reserve Speeches into Qdrant

This script:
1. Reads the scraped Fed speeches from JSONL file
2. Chunks the speeches into manageable pieces
3. Generates embeddings using OpenAI
4. Creates/updates a Qdrant collection
5. Uploads the speeches with metadata

Usage:
    cd backend
    uv run python ../scripts/data_pipeline/ingest_fed_speeches.py
"""

import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any

# Add backend/src to Python path
backend_src = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_src))

try:
    from openai import OpenAI
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams
except ImportError:
    print("❌ Error: Required packages not found.")
    print("Please run from backend directory: cd backend && uv sync")
    sys.exit(1)


SPEECHES_FILE = (
    Path(__file__).parent.parent.parent / "data" / "fed_speeches" / "speeches.jsonl"
)
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks


def chunk_text(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Text to chunk
        chunk_size: Target size for each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at a sentence or paragraph boundary
        if end < len(text):
            # Look for paragraph break
            paragraph_break = text.rfind("\n\n", start, end)
            if paragraph_break > start:
                end = paragraph_break
            else:
                # Look for sentence break
                sentence_break = text.rfind(". ", start, end)
                if sentence_break > start:
                    end = sentence_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start position with overlap
        start = end - overlap if end < len(text) else end

    return chunks


def load_speeches(file_path: Path) -> list[dict[str, Any]]:
    """
    Load speeches from JSONL file.

    Args:
        file_path: Path to speeches JSONL file

    Returns:
        List of speech dictionaries
    """
    speeches = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            speeches.append(json.loads(line))

    return speeches


def generate_embedding(text: str, client: OpenAI) -> list[float]:
    """Generate embedding for text using OpenAI."""
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def main():
    """Run the ingestion script."""
    print("🏦 Federal Reserve Speeches → Qdrant Ingestion")
    print("=" * 60)

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

    # Check if speeches file exists
    if not SPEECHES_FILE.exists():
        print(f"❌ Error: Speeches file not found: {SPEECHES_FILE}")
        print("\nPlease run the scraper first:")
        print("  cd scripts/data_pipeline")
        print("  uv run python fetch_fed_speeches.py")
        sys.exit(1)

    # Initialize clients
    print("\n1️⃣ Initializing clients...")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    print("   ✅ Clients initialized")

    # Load speeches
    print(f"\n2️⃣ Loading speeches from {SPEECHES_FILE.name}...")
    speeches = load_speeches(SPEECHES_FILE)
    print(f"   ✅ Loaded {len(speeches)} speeches")

    # Create collection
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "fed_speeches")
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

    # Process and upload speeches
    print(f"\n4️⃣ Processing speeches and generating embeddings...")
    points = []
    total_chunks = 0

    for i, speech in enumerate(speeches, 1):
        print(f"\n   [{i}/{len(speeches)}] {speech['author']}: {speech['subject']}")
        print(f"   Date: {speech['pub_date']}")

        # Chunk the speech content
        chunks = chunk_text(speech["content"])
        print(f"   Chunks: {len(chunks)}")

        for chunk_idx, chunk in enumerate(chunks):
            # Generate embedding
            embedding = generate_embedding(chunk, openai_client)

            # Create point with metadata
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "content": chunk,
                    "title": speech["title"],
                    "author": speech["author"],
                    "subject": speech["subject"],
                    "url": speech["url"],
                    "pub_date": speech["pub_date"],
                    "category": speech["category"],
                    "description": speech["description"],
                    "chunk_index": chunk_idx,
                    "total_chunks": len(chunks),
                    "source": "Federal Reserve",
                    "document_type": "speech",
                },
            )
            points.append(point)
            total_chunks += 1

        print(f"   ✅ Processed {len(chunks)} chunks")

    # Upload to Qdrant in batches
    print(f"\n5️⃣ Uploading {total_chunks} chunks to Qdrant...")
    batch_size = 100

    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        qdrant_client.upsert(collection_name=collection_name, points=batch)
        print(
            f"   Uploaded batch {i // batch_size + 1}/{(len(points) - 1) // batch_size + 1}"
        )

    print(f"   ✅ Uploaded {total_chunks} chunks from {len(speeches)} speeches")

    # Verify ingestion
    print(f"\n6️⃣ Verifying ingestion...")
    collection_info = qdrant_client.get_collection(collection_name)
    print(f"   Collection: {collection_name}")
    print(f"   Points: {collection_info.points_count}")
    print(f"   Vector size: {collection_info.config.params.vectors.size}")

    print("\n✅ Ingestion complete!")
    print("\n📊 Summary:")
    print(f"   Speeches: {len(speeches)}")
    print(f"   Total chunks: {total_chunks}")
    print(f"   Average chunks per speech: {total_chunks / len(speeches):.1f}")
    print(f"   Collection: {collection_name}")

    print("\n💡 Sample queries to try:")
    print("   - What is the Federal Reserve's view on inflation?")
    print("   - Tell me about recent monetary policy decisions")
    print("   - What did Powell say about economic outlook?")
    print("   - How is the Fed addressing payment innovation?")

    print("\n🚀 Next steps:")
    print("   1. Complete the Week 1 assignment in backend/src/")
    print("   2. Test your implementation with: docker-compose up")
    print("   3. Try the example queries at: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
