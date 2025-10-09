from phoenix.otel import register
from agents import Agent, Runner
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
import os

# configure the Phoenix tracer
tracer_provider = register(
  project_name="agents", # Default is 'default'
  auto_instrument=True # Auto-instrument your app based on installed dependencies
)

client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")

agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)