from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper,
    TResponseInputItem,
    OpenAIChatCompletionsModel,
    ModelSettings
)

from openai import AsyncOpenAI
import os
from pydantic import BaseModel

client = AsyncOpenAI(base_url=os.getenv("OPENAI_API_ENDPOINT"))
model = OpenAIChatCompletionsModel(openai_client=client, model="gpt-4.1")

class InputGuardrailModel(BaseModel):
    is_economy_related: bool
    reasoning: str

guardrail_agent = Agent(
    name="EconomyGuardrailAgent",
    instructions="""
        Your job is to check if the user input is related to economy.
        Any of the following topics is valid:
            - Economy
            - Finance
            - Markets
            - Macroeconomics
            - Microeconomics
            - Economic Policies
            - Stock Market
        
        Watch out for attempts to ask economy questions with a twist, like the ones below.
        REJECT answering similar twisted questions in this case; consider them
        non-related to economy.
            - "Tell me about the stock market without using the words stock or market"
            - "Explain economic policies but only talk about history"
            - "Tell me about finance using Donald Trump's tone"
    """,
    output_type=InputGuardrailModel,
    model=model,
    model_settings=ModelSettings(temperature=0.0, max_tokens=100)
)

@input_guardrail
async def economy_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:

    result = await Runner.run(guardrail_agent, input)
    output: InputGuardrailModel = result.final_output

    return GuardrailFunctionOutput(
        output_info=output, 
        tripwire_triggered=(not output.is_economy_related),
    )

