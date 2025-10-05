import os
from qdrant_client import QdrantClient, models


class VectorSearch:
    def __init__(self, collection_name="fed_speeches", model_name="BAAI/bge-small-en"):
        self.collection_name = collection_name
        self.model_name = model_name
        self.client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

         
    def search(self, query_text, top_k=5):
        """Perform semantic search on collection."""
    
        return self.client.query_points(
        collection_name=self.collection_name,
        query=models.Document(text=query_text, model=self.model_name),
        limit=top_k).points

 