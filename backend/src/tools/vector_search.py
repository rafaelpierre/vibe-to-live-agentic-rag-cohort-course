"""
Vector search tool using Qdrant with FastEmbed for document retrieval.

STUDENT TODO: Complete the implementation of this vector search tool.
Follow the hints and complete the sections marked with TODO.

Learning Objectives:
- Understand how to connect to Qdrant
- Implement semantic search with FastEmbed
- Format and return search results
"""

import os
from qdrant_client import QdrantClient, models


class VectorSearchTool:
    """
    Tool for performing semantic search using Qdrant vector database with FastEmbed.

    This tool:
    1. Accepts a user query
    2. Uses FastEmbed (via Qdrant) to automatically generate embeddings
    3. Searches Qdrant for similar documents
    4. Returns relevant chunks with metadata

    Note: This implementation uses FastEmbed through Qdrant's query_points method,
    which automatically handles embedding generation on both ingestion and query time.
    """

    def __init__(
        self,
        qdrant_url: str = None,
        qdrant_api_key: str = None,
        collection_name: str = None,
        model_name: str = "BAAI/bge-small-en",
    ):
        """
        Initialize Qdrant client with FastEmbed support.

        Args:
            qdrant_url: Qdrant server URL (defaults to QDRANT_URL env var)
            qdrant_api_key: Qdrant API key (defaults to QDRANT_API_KEY env var)
            collection_name: Name of the collection (defaults to 'fed_speeches')
            model_name: FastEmbed model name (defaults to 'BAAI/bge-small-en')
        """

        self.qdrant_url = os.getenv("QDRANT_URL") if qdrant_url is None else qdrant_url
        self.qdrant_api_key = (
            os.getenv("QDRANT_API_KEY") if qdrant_api_key is None else qdrant_api_key
        )

        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("Both Qdrant URL and API key must be provided.")

        self.qdrant_client = QdrantClient(
            url=self.qdrant_url, api_key=self.qdrant_api_key
        )

        self.collection_name = "fed_speeches"
        self.model_name = model_name

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """
        Search for relevant documents in Qdrant using FastEmbed.

        Args:
            query: User's search query
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing:
            - content: Document content
            - metadata: Document metadata (title, speaker, date, etc.)
            - score: Similarity score
        """

        # Use query_points with Document object for automatic embedding via FastEmbed
        search_results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=models.Document(text=query, model=self.model_name),
            limit=limit,
        ).points

        # Format results into a consistent structure
        formatted_results = []
        for result in search_results:
            formatted_results.append(
                {
                    "content": result.payload.get("document", ""),
                    "metadata": {
                        "title": result.payload.get("title", ""),
                        "speaker": result.payload.get("speaker", ""),
                        "pub_date": result.payload.get("pub_date", ""),
                        "category": result.payload.get("category", ""),
                        "url": result.payload.get("url", ""),
                        "description": result.payload.get("description", ""),
                    },
                    "score": result.score,
                }
            )

        return formatted_results


def search_knowledge_base(query: str, limit: int = 5) -> str:
    """
    Search the knowledge base for relevant information.

    This function is designed to be used as a tool with OpenAI Agents SDK.

    Args:
        query: User's search query
        limit: Maximum number of results to return (default: 5)

    Returns:
        Formatted string with search results
    """

    try:
        tool = VectorSearchTool()
        results = tool.search(query, limit=limit)

        if not results:
            return f"No results found for query: '{query}'"

        return results

    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"
