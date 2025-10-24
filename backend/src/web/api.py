from fastapi import FastAPI
from pydantic import BaseModel
from src.agent.models import AgentResponse
from src.web.services import get_chat_response


app = FastAPI()

class ChatRequest(BaseModel):
    message: str


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat")
async def chat(request: ChatRequest) -> AgentResponse:
    
    await get_chat_response(prompt=request.message)
