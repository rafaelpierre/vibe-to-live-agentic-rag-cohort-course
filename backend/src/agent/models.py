from pydantic import BaseModel
from textwrap import dedent

class AgentResponse(BaseModel):
    answer: str
    sources: list[str]

    def __str__(self):
        return dedent(f"""
            Answer: {self.answer}\n
            Sources: {self.sources}
        """)