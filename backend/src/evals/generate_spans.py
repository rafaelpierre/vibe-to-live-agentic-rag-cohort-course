import asyncio
import pandas as pd
from src.web.services import get_chat_response
from typing import List
from src.agent.rag_agent import model
from agents import Agent, Runner, ModelSettings


async def generate_input_queries(max_queries: int = 20) -> List[str]:
    """Generates synthetic queries to mimick a human asking questions.

    Args:
        max_queries: Maximum number of queries to generate
    """

    async def generate_single_query(i: int) -> str:
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
        return response.final_output

    tasks = [generate_single_query(i) for i in range(max_queries)]
    queries = await asyncio.gather(*tasks)
    return list(queries)


async def generate_responses(queries: List[str]) -> pd.DataFrame:
    """Pipeline for running our agentic loop with synthetic queries as input

    Args:
        queries: List of synthetic queries
        
    Returns:
        DataFrame with input queries and output responses
    """

    tasks = [get_chat_response(prompt=query) for query in queries]
    results = await asyncio.gather(*tasks)
    
    # Create DataFrame with the expected structure for evaluation
    data = []
    for i, (query, response) in enumerate(zip(queries, results)):
        data.append({
            'context.span_id': f'span_{i}',
            'input.value': query,
            'output.value': str(response)
        })
    
    return pd.DataFrame(data)