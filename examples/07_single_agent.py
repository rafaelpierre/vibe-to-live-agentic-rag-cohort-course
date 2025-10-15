from phoenix.otel import register
from agents import (
  Agent,
  Runner,
  OpenAIChatCompletionsModel,
  function_tool,
  ModelSettings,
  SQLiteSession
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from openai import AsyncOpenAI
import os
from datetime import datetime
import asyncio
import random

# configure the Phoenix tracer
tracer_provider = register(
  project_name="single-agent-sync-tool-calls",
  auto_instrument=True
)

from pydantic import BaseModel

class AgentOutput(BaseModel):
    synthesized_answer: str
    sources: list[str]


client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")
session = SQLiteSession("conversation_123")


@function_tool
async def search(query: str, top_k: int = 1) -> str:
    """Mimicks a search engine for information based on the query.
    Args:
        query (str): The search query.
        top_k (int, optional): The number of top results to return. Defaults to 1.
    Returns:
        str: The search results.
    """

    await asyncio.sleep(1)  # Simulate API delay

    fed_speeches_synthetic = [
        "The time has come for policy to adjust. The direction of travel is clear, and the timing and pace of rate cuts will depend on incoming data, the evolving outlook, and the balance of risks.",
        "The labor market has shown remarkable resilience, with unemployment remaining low despite our efforts to cool demand. However, we are seeing signs of gradual rebalancing as job openings decline and wage growth moderates.",
        "Higher interest rates have tested the resilience of our financial system. While most institutions have weathered this transition well, we must remain vigilant about vulnerabilities in commercial real estate and certain non-bank financial intermediaries.",
        "As we explore the potential for a central bank digital currency, we must carefully consider the implications for monetary policy transmission, financial stability, and privacy. Any digital dollar must complement, not replace, existing payment systems.",
        "Economic recovery has been uneven across regions and demographic groups. While aggregate data shows strength, we must not lose sight of communities still struggling with inflation's impact on purchasing power, particularly in housing and essentials.",
        "Climate change poses emerging risks to financial stability and the broader economy. As a central bank, our responsibility is to ensure financial institutions understand and manage these risks appropriately within our existing mandate.",
        "Supply chains have largely normalized from their pandemic-era disruptions. This improvement, combined with moderating demand, has been a key factor in the disinflation process. However, geopolitical tensions remain a risk to continued progress.",
        "The bank stress events of 2023 revealed vulnerabilities in interest rate risk management and the speed of digital bank runs. We have strengthened supervisory expectations around liquidity management and are enhancing our monitoring of uninsured deposits.",
        "Recent data suggests we may be seeing a pickup in productivity growth, potentially driven by technological adoption and business process improvements. If sustained, this could allow for higher non-inflationary growth and would be welcome news for living standards.",
        "The dollar's strength reflects both our relative economic performance and the Federal Reserve's monetary policy stance. While a strong dollar has benefits, it also affects emerging markets and can create spillovers that eventually impact the U.S. economy through trade and financial channels."
    ]

    search_results = {"result": random.choice(fed_speeches_synthetic) for _ in range(top_k)}
    return f"{datetime.now()} - Search results for '{query}': {search_results.get('result', 'No results found.')}."

rag_agent = Agent(
  name="RAGAgent",
  instructions=f"""
    {RECOMMENDED_PROMPT_PREFIX}
    You are a helpful assistant that synthesizes information from multiple sources
    to provide a comprehensive answer to the user's question.
    
    Think step by step:

    1. User will enter a question in natural language.
    2. Understand the question and generate 3 different search queries that would help find relevant information.
    3. Use the `search` tool to retrieve information for each of the generated queries.
    4. Synthesize the information retrieved from the `search` tool calls to formulate a comprehensive response.
    5. Provide the final answer along with the sources used.
    """,
  model=model,
  output_type=AgentOutput,
  tools = [search],
  model_settings=ModelSettings(
      tool_choice = "required",
      top_k = 5,
      max_tokens = 1000
    )
)


async def main():
    user_input = "What factors are impacting interest rates?"
    result = await Runner.run(rag_agent, user_input, session=session)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())