import logging
from textwrap import dedent
import os
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool,
    ModelSettings
)
from openai import AsyncOpenAI
from src.tools.vector_search import search_knowledge_base
from src.agents.models import AgentResponse


client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")


@function_tool
async def search(query: str) -> str:
    """Perform semantic search on Fed speeches collection."""
    results = search_knowledge_base(query)
    return results


agent = Agent(
    name="FedSpeechAgent",
    instructions=dedent(
        """
        Use the provided functions to answer questions about Federal Reserve speeches.
        Always cite your sources from the search results.
        """,
    ),
    model=model,
    tools=[search],
    model_settings=ModelSettings(tool_choice = "search"),
    output_type=AgentResponse
)