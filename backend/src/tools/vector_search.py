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
        # TODO 1: Get credentials from environment variables or use provided parameters
        # Hint: Use os.getenv("VARIABLE_NAME") to read environment variables
        # Hint: Use the 'or' operator to fallback to parameters if env var is not set
        # Example: self.qdrant_url = qdrant_url or os.getenv("QDRANT_URL")
        
        self.qdrant_url = None  # TODO: Replace with actual implementation
        self.qdrant_api_key = None  # TODO: Replace with actual implementation
        
        # TODO 2: Validate that both URL and API key are provided
        # Hint: Check if either is None or empty, then raise ValueError
        # Hint: Use an if statement to check: if not self.qdrant_url or not self.qdrant_api_key:
        
        # TODO: Add validation here
        
        # TODO 3: Initialize the Qdrant client
        # Hint: Create a QdrantClient instance with url and api_key parameters
        # Example: self.qdrant_client = QdrantClient(url=..., api_key=...)
        
        self.qdrant_client = None  # TODO: Replace with actual QdrantClient initialization
        
        # TODO 4: Set collection name and model name with defaults
        # Hint: Use the same pattern as above - use provided value or default
        # Default collection_name: "fed_speeches"
        # Default model_name is already set in the function signature
        
        self.collection_name = None  # TODO: Replace with actual implementation
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
        # TODO 5: Perform search using Qdrant's query_points method
        # Hint: Use self.qdrant_client.query_points() with the following parameters:
        #   - collection_name: self.collection_name
        #   - query: models.Document(text=query, model=self.model_name)
        #   - limit: limit
        # Hint: The result has a .points attribute that contains the list of results
        # Example: results = self.qdrant_client.query_points(...).points
        
        search_results = []  # TODO: Replace with actual query_points call
        
        # TODO 6: Format results into a list of dictionaries
        # Hint: Loop through search_results and extract information
        # Hint: Each result has .payload (dict) and .score (float) attributes
        # Hint: Use result.payload.get("key", "") to safely get values with defaults
        
        formatted_results = []
        # TODO: Add your loop here to format results
        # Each formatted result should be a dict with keys: "content", "metadata", "score"
        # metadata should include: title, speaker, pub_date, category, url, description
        
        return formatted_results

    def verify_collection(self) -> dict:
        """
        Verify that the collection exists and return its info.
        
        Returns:
            Dictionary with collection information
        """
        # TODO 7: Try to get collection info and handle errors
        # Hint: Use a try/except block
        # Hint: Call self.qdrant_client.get_collection(self.collection_name)
        # Hint: If successful, return a dict with exists=True and collection info
        # Hint: If an exception occurs, return a dict with exists=False and error message
        
        try:
            # TODO: Call get_collection and extract info
            # collection_info = ...
            # Return dict with: exists, points_count, vector_size, distance
            pass
        except Exception as e:
            # TODO: Return error dict
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
    # TODO 8: Implement the search_knowledge_base function
    # Hint: This function wraps VectorSearchTool for use with OpenAI Agents
    # Hint: Use a try/except block to handle errors gracefully
    
    try:
        # TODO: Create VectorSearchTool instance
        # tool = VectorSearchTool()
        
        # TODO: Perform search
        # results = tool.search(query, limit=limit)
        
        # TODO: Check if results are empty
        # if not results:
        #     return f"No results found for query: '{query}'"
        
        # TODO: Format results as a readable string
        # Include: number of documents, and for each result:
        #   - Result number and score
        #   - Title, Speaker, Date, Category
        #   - Content snippet (first 300 characters)
        
        return "TODO: Implement search_knowledge_base"
        
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

