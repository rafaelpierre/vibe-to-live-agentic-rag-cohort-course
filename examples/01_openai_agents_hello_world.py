import asyncio

from agents import Agent, Runner, set_tracing_disabled
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os

set_tracing_disabled(True)

client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=model,
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":
    asyncio.run(main())