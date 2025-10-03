"""
Vector search tool using Qdrant for document retrieval.
"""

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, SearchRequest, VectorParams

from ..config import settings


class VectorSearchTool:
    """
    Tool for performing semantic search using Qdrant vector database.

    This tool:
    1. Accepts a user query
    2. Generates an embedding using OpenAI
    3. Searches Qdrant for similar documents
    4. Returns relevant chunks with metadata
    """

    def __init__(self):
        """Initialize Qdrant client and OpenAI client."""
        # TODO: Initialize Qdrant client
        # Hint: Use QdrantClient with url and api_key from settings
        self.qdrant_client = None

        # TODO: Initialize OpenAI client
        # Hint: Use OpenAI() with api_key from settings
        self.openai_client = None

        self.collection_name = settings.qdrant_collection_name
        self.embedding_model = "text-embedding-3-small"

    def _generate_embedding(self, text: str) -> list[float]:
        """
        Generate embedding vector for the given text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats

        TODO: Implement this method
        Hint: Use self.openai_client.embeddings.create()
        """
        # TODO: Generate embedding using OpenAI API
        # response = self.openai_client.embeddings.create(...)
        # return response.data[0].embedding
        raise NotImplementedError("Students need to implement embedding generation")

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """
        Search for relevant documents in Qdrant.

        Args:
            query: User's search query
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing:
            - content: Document content
            - metadata: Document metadata (source, page, etc.)
            - score: Similarity score

        TODO: Implement this method
        Hint:
        1. Generate embedding for query using _generate_embedding()
        2. Search Qdrant using self.qdrant_client.search()
        3. Format and return results
        """
        # TODO: Implement vector search
        # 1. query_vector = self._generate_embedding(query)
        # 2. results = self.qdrant_client.search(...)
        # 3. Format results with content, metadata, and score
        raise NotImplementedError("Students need to implement vector search")

    def create_collection(self, vector_size: int = 1536):
        """
        Create a Qdrant collection if it doesn't exist.

        Args:
            vector_size: Dimension of embedding vectors (1536 for text-embedding-3-small)

        This is a helper method for initial setup.
        In production, collections are typically created separately.
        """
        try:
            self.qdrant_client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists")
        except Exception:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print(f"Collection '{self.collection_name}' created successfully")


# Tool function for OpenAI Agents SDK
def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant information.

    This function is designed to be used as a tool with OpenAI Agents SDK.

    Args:
        query: User's search query

    Returns:
        Formatted string with search results

    TODO: Implement this function
    Hint:
    1. Create VectorSearchTool instance
    2. Call search() method
    3. Format results as a readable string
    """
    # TODO: Implement tool function
    # tool = VectorSearchTool()
    # results = tool.search(query)
    # return formatted_string
    return "TODO: Implement knowledge base search"
