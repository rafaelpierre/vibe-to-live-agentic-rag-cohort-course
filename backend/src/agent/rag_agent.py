from textwrap import dedent
import os
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    OpenAIChatCompletionsModel,
    function_tool,
    ModelSettings,
)
from openai import AsyncOpenAI
from src.tools.vector_search import search_knowledge_base
from src.agent.models import AgentResponse
from src.guardrails.input_guardrails import economy_guardrail


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
        Don't answer a question in case no results were returned from the search. If that's
        the case, just say that you couldn't find any relevant information.

        - Don't use markdown.
        - Make sure to keep the answer in the "answer" field, and the sources in the "sources" field as a list.
        """,
    ),
    model=model,
    tools=[search],
    model_settings=ModelSettings(tool_choice="search"),
    output_type=AgentResponse,
    input_guardrails=[economy_guardrail],
)
