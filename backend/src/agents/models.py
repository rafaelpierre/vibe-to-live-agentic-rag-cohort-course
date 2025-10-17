from pydantic import BaseModel

class AgentResponse(BaseModel):
    answer: str
    sources: list[str]