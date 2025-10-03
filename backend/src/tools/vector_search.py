"""
Vector search tool using Qdrant with FastEmbed for document retrieval.
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
        model_name: str = "BAAI/bge-small-en"
    ):
        """
        Initialize Qdrant client with FastEmbed support.
        
        Args:
            qdrant_url: Qdrant server URL (defaults to QDRANT_URL env var)
            qdrant_api_key: Qdrant API key (defaults to QDRANT_API_KEY env var)
            collection_name: Name of the collection (defaults to 'fed_speeches')
            model_name: FastEmbed model name (defaults to 'BAAI/bge-small-en')
        """
        # Get credentials from environment or parameters
        self.qdrant_url = qdrant_url or os.getenv("QDRANT_URL")
        self.qdrant_api_key = qdrant_api_key or os.getenv("QDRANT_API_KEY")
        
        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY must be provided or set as environment variables")
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
        )
        
        self.collection_name = collection_name or "fed_speeches"
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
            limit=limit
        ).points
        
        # Format results into a consistent structure
        formatted_results = []
        for result in search_results:
            formatted_results.append({
                "content": result.payload.get("document", ""),
                "metadata": {
                    "title": result.payload.get("title", ""),
                    "speaker": result.payload.get("speaker", ""),
                    "pub_date": result.payload.get("pub_date", ""),
                    "category": result.payload.get("category", ""),
                    "url": result.payload.get("url", ""),
                    "description": result.payload.get("description", ""),
                },
                "score": result.score
            })
        
        return formatted_results

    def verify_collection(self) -> dict:
        """
        Verify that the collection exists and return its info.
        
        Returns:
            Dictionary with collection information
        """
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "exists": True,
                "points_count": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance
            }
        except Exception as e:
            return {
                "exists": False,
                "error": str(e)
            }


# Tool function for OpenAI Agents SDK
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
        # Create VectorSearchTool instance
        tool = VectorSearchTool()
        
        # Perform search
        results = tool.search(query, limit=limit)
        
        # Format results as a readable string
        if not results:
            return f"No results found for query: '{query}'"
        
        formatted_output = f"Found {len(results)} relevant documents:\n\n"
        
        for idx, result in enumerate(results, 1):
            formatted_output += f"--- Result {idx} (Score: {result['score']:.4f}) ---\n"
            formatted_output += f"Title: {result['metadata']['title']}\n"
            formatted_output += f"Speaker: {result['metadata']['speaker']}\n"
            formatted_output += f"Date: {result['metadata']['pub_date']}\n"
            formatted_output += f"Category: {result['metadata']['category']}\n"
            
            # Include a snippet of the content (first 300 characters)
            content = result['content']
            snippet = content[:300] + "..." if len(content) > 300 else content
            formatted_output += f"Content: {snippet}\n\n"
        
        return formatted_output
        
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

