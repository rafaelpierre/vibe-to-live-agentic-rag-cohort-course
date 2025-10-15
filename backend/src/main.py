"""
FastAPI application for Agentic RAG API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .agents.rag_agent import create_rag_agent
from .schemas.requests import ChatRequest, ChatResponse, HealthResponse

# Initialize FastAPI app
app = FastAPI(
    title="Agentic RAG API",
    description="Production-ready RAG API with OpenAI Agents SDK",
    version="0.1.0",
    debug=True,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG agent (lazy loading in production would be better)
rag_agent = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global rag_agent
    # TODO: Initialize the RAG agent
    # Hint: Use create_rag_agent() function
    # rag_agent = create_rag_agent()
    print("⚠️  TODO: Initialize RAG agent in startup_event()")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print(f"👋 Shutting down...")


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint returning API information."""
    return HealthResponse(status="healthy", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.1.0")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint for RAG agent interactions.

    Args:
        request: ChatRequest with query and optional session_id

    Returns:
        ChatResponse with answer, sources, and session_id

    TODO: Implement this endpoint
    Steps:
    1. Validate the request (already done by FastAPI/Pydantic)
    2. Call the RAG agent with the query
    3. Format and return the response
    4. Handle errors appropriately
    """
    # TODO: Implement chat endpoint
    # Example structure:
    # try:
    #     result = await rag_agent.chat(
    #         query=request.query,
    #         session_id=request.session_id
    #     )
    #     return ChatResponse(**result)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(
        status_code=501,
        detail="TODO: Implement /chat endpoint - this is your Week 1 assignment!",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000)
