import asyncio

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
import os

set_tracing_disabled(True)

client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")

# The agent below should answer questions related to Federal Reserve speeches.
# It is still incomplete:
# - Add specific instructions for the agent to follow when answering questions.
# - Add a function tool that performs vector search, and pass it to the agent
# - Tip: there are different function tool execution modes

async def main():
    agent = Agent(
        name="FedSpeechAgent",
        instructions="",
        model=model
    )

    result = await Runner.run(agent, "What's the fed overview about monetary policy as of August 2025?")
    return result.final_output

if __name__ == "__main__":
    
    result = asyncio.run(main())
    print(result)