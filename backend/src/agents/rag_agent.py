import asyncio
import os
import sys
from pathlib import Path

# Import from openai-agents library BEFORE adding src to path
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from openai import AsyncOpenAI

# Add src to path for local imports
if __name__ == "__main__":
    src_path = Path(__file__).parent.parent
    sys.path.insert(0, str(src_path))


import logging

logging.basicConfig(level=logging.INFO)

from tools.vector_search import VectorSearchTool, search_knowledge_base

set_tracing_disabled(True)

client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")

# The agent below should answer questions related to Federal Reserve speeches.
# It is still incomplete:
# - Add specific instructions for the agent to follow when answering questions.
# - Add a function tool that performs vector search, and pass it to the agent
# - Tip: there are different function tool execution modes

async def main():
    @function_tool
    async def search_knowledge_base(query: str) -> str:
        """Perform semantic search on Fed speeches collection."""
        results = search_knowledge_base(query)
        return results
    agent = Agent(
        name="FedSpeechAgent",
        instructions="Use the provided functions to answer questions about Federal Reserve speeches. Always cite your sources from the search results.",
        model=model,
        tools=[search_knowledge_base],
        model_settings={"tool_execution_mode": "auto"}  # or "manual"
    )

    result = await Runner.run(agent, "What's the fed overview about monetary policy as of August 2025?")
    return result.final_output

if __name__ == "__main__":
    
    result = asyncio.run(main())
    print(result)