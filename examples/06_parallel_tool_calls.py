from phoenix.otel import register
from agents import (
  Agent,
  Runner,
  OpenAIChatCompletionsModel,
  function_tool,
  ModelSettings
)
from openai import AsyncOpenAI
import os

# configure the Phoenix tracer
tracer_provider = register(
  project_name="paralell-tool-calls",
  auto_instrument=True
)

@function_tool
async def get_weather(location: str) -> str:
    """Get the current weather for a given location.
    Args:
        location (str): The location to get the weather for. E.g., "NYC", "SFO", "AMS"
    Returns:
        str: A string describing the current weather.
    """

    weather_data = {
        "NYC": "sunny, 75°F",
        "SFO": "foggy, 60°F",
        "AMS": "cloudy, 55°F"
    }

    return f"The current weather in {location} is {weather_data.get(location, 'unknown')}."



client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")

agent = Agent(
  name="WeatherBot",
  instructions="You are a helpful assistant that can provide weather information.",
  model=model,
  model_settings=ModelSettings(parallel_tool_calls=True),
  tools=[get_weather]
)


result = Runner.run_sync(agent, "Tell me the weather in NYC, SFO, and AMS.")
print(result.final_output)