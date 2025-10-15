import asyncio

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from datetime import datetime
from qdrant_client import QdrantClient, models

set_tracing_disabled(True)

client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")

@function_tool
def get_current_time() -> str:
    """Get the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def semantic_search(query_text: str) -> str:
    """Perform semantic search on Fed speeches collection."""
    
    # Configuration
    COLLECTION_NAME = "fed_speeches"
    MODEL_NAME = "BAAI/bge-small-en"
    
    # Get Qdrant credentials from environment variables
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    
    if not QDRANT_URL or not QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set")
    
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    
    print(f"🔍 Query: '{query_text}'\n")
    
    # Perform search using Document object with FastEmbed
    # FastEmbed automatically generates the query embedding
    search_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=models.Document(text=query_text, model=MODEL_NAME),
        limit=5
    ).points
    return search_results


async def main(prompt: str = "What did the Fed say about inflation in their recent speeches?"):
    agent = Agent(
        name="Assistant",
        instructions="You are an agent that can call functions to get information.",
            model=model,
            tools=[get_current_time, semantic_search],
    )

    result = await Runner.run(agent, prompt)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())