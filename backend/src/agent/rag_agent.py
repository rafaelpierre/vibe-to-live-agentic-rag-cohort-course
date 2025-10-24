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
    """Perform semantic search on the Federal Reserve speeches knowledge base.

    This async function serves as the primary tool available to the RAG agent for
    retrieving relevant information from the indexed Federal Reserve speeches collection.
    It's decorated with @function_tool to make it available as a callable tool within
    the PydanticAI agent framework.

    The function acts as a wrapper around the vector_search module's search_knowledge_base
    function, providing semantic (meaning-based) search rather than keyword matching.
    This enables the agent to find relevant speeches even when the exact terminology
    differs between the query and the source documents.

    The search is performed against a vector database (Qdrant) containing embedded
    representations of Federal Reserve speeches, allowing for semantic similarity
    matching between the query and the speech content.

    Args:
        query (str): The search query string. This is typically a question or topic
            related to Federal Reserve policies, speeches, or economic commentary.
            The query will be embedded and compared against the vector representations
            of the speech documents to find semantically similar content.

    Returns:
        str: A formatted string containing the search results. The exact format
            depends on the search_knowledge_base implementation, but typically includes
            relevant excerpts from Federal Reserve speeches along with metadata such
            as speaker, date, and source document identifiers.

    Example:
        >>> results = await search("What is the Fed's position on inflation?")
        >>> print(results)
        # Returns formatted search results from Fed speeches about inflation

    Note:
        - This is an async function and must be awaited
        - Decorated with @function_tool to integrate with PydanticAI agent framework
        - Uses semantic search via vector embeddings, not keyword matching
        - The agent is configured with tool_choice="search" to prioritize this tool
        - Results are passed back to the LLM for synthesis into a final answer
        - Depends on QDRANT_URL, QDRANT_API_KEY, and other vector store configuration
    """
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
