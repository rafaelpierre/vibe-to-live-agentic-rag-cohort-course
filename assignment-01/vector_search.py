import os
from qdrant_client import QdrantClient, models
from agents import function_tool

collection_name = "fed_speeches"
model_name = "BAAI/bge-small-en"

@function_tool(description="Perform semantic search on collection.")
def searchCollection(query_text, top_k=5):
    """Perform semantic search on collection."""
    
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),   
    )
    
    return client.query_points(
        collection_name=collection_name,
        query=models.Document(text=query_text, model=model_name),
        limit=top_k).points

 