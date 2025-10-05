import asyncio

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from datetime import datetime

set_tracing_disabled(True)

client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")

@function_tool
def get_current_time() -> str:
    """Get the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def main(prompt: str = "What is the current time?"):
    agent = Agent(
        name="Assistant",
        instructions="You are an agent that can call functions to get information.",
        model=model,
        tools=[get_current_time],
    )

    result = await Runner.run(agent, prompt)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())