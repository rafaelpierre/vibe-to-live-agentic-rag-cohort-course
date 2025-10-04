"""
Request and response schemas for the API.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request model for the /chat endpoint.
    """

    query: str = Field(
        ...,
        description="User's question or query",
        min_length=1,
        max_length=1000,
        examples=["What are the key features of OpenAI Agents SDK?"],
    )

    session_id: str | None = Field(
        default=None,
        description="Optional session ID for conversation continuity",
        examples=["user-123-session-456"],
    )


class ChatResponse(BaseModel):
    """
    Response model for the /chat endpoint.
    """

    answer: str = Field(..., description="The agent's response to the user's query")

    sources: list[dict[str, str]] | None = Field(
        default=None,
        description="List of sources used to generate the answer",
        examples=[
            [
                {
                    "document": "openai_agents_guide.md",
                    "chunk": "OpenAI Agents SDK provides...",
                    "score": "0.85",
                }
            ]
        ],
    )

    session_id: str | None = Field(
        default=None, description="Session ID for this conversation"
    )


class HealthResponse(BaseModel):
    """
    Response model for the /health endpoint.
    """

    status: str = Field(default="healthy", description="Health status of the service")

    version: str = Field(default="0.1.0", description="API version")
