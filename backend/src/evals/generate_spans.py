import asyncio
from src.web.services import get_chat_response
from typing import List
from src.agent.rag_agent import model
from agents import Agent, Runner, ModelSettings


async def generate_input_queries(max_queries: int = 20) -> List[str]:
    """Generates synthetic queries to mimick a human asking questions.

    Args:
        max_queries: Maximum number of queries to generate
    """

    queries = []
    for i in range(max_queries):
        prompt = f"Generate a synthetic query {i+1} related to Federal Reserve speeches."
        response = await Runner.run(
            Agent(
                name="QueryGenerator",
                instructions="""
                    Generate a concise and relevant question about Federal Reserve speeches.
                    IMPORTANT: your job is to generate ONE question only, do not provide answers nor any other comment.
                """,
                model=model,
                model_settings=ModelSettings(temperature=0.7, max_tokens=50)
            ),
            prompt
        )
        queries.append(response.final_output)

    return queries


async def pipeline(queries: List[str]) -> List[str]:
    """Pipeline for running our agentic loop with synthetic queries as input

    Args:
        queries: List of synthetic queries
    """

    tasks = [get_chat_response(prompt=query) for query in queries]
    results = await asyncio.gather(*tasks)
    return [str(result) for result in results]