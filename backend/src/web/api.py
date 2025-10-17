from fastapi import FastAPI
from pydantic import BaseModel
from agents import Runner
from src.agents.rag_agent import agent
from src.agents.models import AgentResponse
from phoenix.otel import register

app = FastAPI()

tracer_provider = register(
  project_name="fast_api_agent", # Default is 'default'
  auto_instrument=True # Auto-instrument your app based on installed dependencies
)

class ChatRequest(BaseModel):
    message: str


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat")
async def chat(request: ChatRequest) -> AgentResponse:

    result = await Runner.run(agent, request.message)
    return result.final_output