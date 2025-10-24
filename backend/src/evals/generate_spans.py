import asyncio
import pandas as pd
from src.web.services import get_chat_response
from typing import List
from src.agent.rag_agent import model
from agents import Agent, Runner, ModelSettings


async def generate_input_queries(max_queries: int = 20) -> List[str]:
    """Generate synthetic input queries to mimic human questions about Federal Reserve speeches.

    This async function creates a specified number of synthetic queries using an AI agent.
    Each query is generated independently and concurrently using asyncio.gather for
    efficiency. The queries are designed to simulate realistic user questions about
    Federal Reserve speeches, policies, and economic topics.

    The function uses the PydanticAI library with an agent configured to generate
    single, concise questions. Temperature is set to 0.7 to provide creative variety
    while maintaining relevance, and max_tokens is limited to 50 to keep queries concise.

    Args:
        max_queries (int): The maximum number of synthetic queries to generate.
            Each query is generated as an independent async task. Defaults to 20.

    Returns:
        List[str]: A list of synthetic query strings, each representing a question
            about Federal Reserve speeches. The list will have exactly max_queries
            elements unless an error occurs during generation.

    Example:
        >>> queries = await generate_input_queries(max_queries=5)
        >>> print(queries[0])
        "What did the Federal Reserve say about inflation in recent speeches?"

    Note:
        - This is an async function and must be awaited
        - Uses the global 'model' object from src.agent.rag_agent
        - All queries are generated concurrently for performance
        - Each query is independent; no context is shared between queries
        - Temperature of 0.7 balances creativity with relevance
    """

    async def generate_single_query(i: int) -> str:
        prompt = (
            f"Generate a synthetic query {i + 1} related to Federal Reserve speeches."
        )
        response = await Runner.run(
            Agent(
                name="QueryGenerator",
                instructions="""
                    Generate a concise and relevant question about Federal Reserve speeches.
                    IMPORTANT: your job is to generate ONE question only, do not provide answers nor any other comment.
                """,
                model=model,
                model_settings=ModelSettings(temperature=0.7, max_tokens=50),
            ),
            prompt,
        )
        return response.final_output

    tasks = [generate_single_query(i) for i in range(max_queries)]
    queries = await asyncio.gather(*tasks)
    return list(queries)


async def generate_responses(queries: List[str]) -> pd.DataFrame:
    """Execute the agentic RAG pipeline with synthetic queries and return structured results.

    This async function takes a list of input queries and runs each through the complete
    RAG (Retrieval-Augmented Generation) agent pipeline to generate responses. The function
    processes all queries concurrently using asyncio.gather for efficiency, then structures
    the results into a pandas DataFrame format that matches the expected schema for
    downstream evaluation tasks.

    Each query-response pair is assigned a unique span_id for traceability, and the
    DataFrame is structured to match the format expected by Phoenix evaluation tools,
    with columns for span context, input queries, and output responses.

    Args:
        queries (List[str]): A list of query strings to process through the RAG agent.
            Each query will trigger the full agentic workflow including vector search,
            context retrieval, and LLM-based response generation.

    Returns:
        pd.DataFrame: A DataFrame containing the evaluation-ready data with columns:
            - 'context.span_id': Unique identifier for each query-response pair (e.g., 'span_0')
            - 'input.value': The original input query string
            - 'output.value': The agent's response as a string

            The DataFrame has one row per query-response pair and is immediately ready
            for use with evaluation functions like evaluate_relevance().

    Example:
        >>> queries = ["What is the Fed's stance on interest rates?", "Explain quantitative easing"]
        >>> results_df = await generate_responses(queries)
        >>> print(results_df.columns)
        Index(['context.span_id', 'input.value', 'output.value'])
        >>> print(len(results_df))
        2

    Note:
        - This is an async function and must be awaited
        - All queries are processed concurrently for performance
        - Uses get_chat_response from src.web.services
        - Response objects are converted to strings for storage
        - Span IDs are sequential integers starting from 0
    """

    tasks = [get_chat_response(prompt=query) for query in queries]
    results = await asyncio.gather(*tasks)

    # Create DataFrame with the expected structure for evaluation
    data = []
    for i, (query, response) in enumerate(zip(queries, results)):
        data.append(
            {
                "context.span_id": f"span_{i}",
                "input.value": query,
                "output.value": str(response),
            }
        )

    return pd.DataFrame(data)
