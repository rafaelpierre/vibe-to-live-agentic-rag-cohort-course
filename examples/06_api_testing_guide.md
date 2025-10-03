# Example: Testing the API with curl

This file contains example curl commands for testing your RAG API.

## Prerequisites

1. Start the API server:
   ```bash
   # Option 1: Development mode
   cd backend
   uv run uvicorn src.main:app --reload

   # Option 2: Docker
   docker-compose up
   ```

2. Make sure you've populated Qdrant:
   ```bash
   cd backend
   uv run python ../scripts/setup_qdrant.py
   ```

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Root Endpoint

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Chat Endpoint (Main Assignment)

#### Simple Query

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the OpenAI Agents SDK?"
  }'
```

#### Query with Session ID

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does RAG work?",
    "session_id": "user-123-session-abc"
  }'
```

#### Follow-up Query (Same Session)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Can you explain that in simpler terms?",
    "session_id": "user-123-session-abc"
  }'
```

## Example Queries

### About OpenAI Agents

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the key features of OpenAI Agents SDK?"}'
```

### About RAG

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain how RAG combines retrieval and generation"}'
```

### About Qdrant

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the benefits of using Qdrant for vector search?"}'
```

### About FastAPI

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Why should I use FastAPI for AI applications?"}'
```

### About Docker

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How does Docker help with production deployments?"}'
```

### About Production AI

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the key considerations for production AI systems?"}'
```

## Testing with httpie (Alternative)

If you have httpie installed:

```bash
# Simple query
http POST localhost:8000/chat query="What is RAG?"

# With session
http POST localhost:8000/chat \
  query="Tell me about vector databases" \
  session_id="test-session-1"
```

## Testing with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"query": "What is the OpenAI Agents SDK?"}
)

print(response.json())
```

## Expected Response Format

Successful response:
```json
{
  "answer": "The OpenAI Agents SDK is a powerful framework for building autonomous AI agents...",
  "sources": [
    {
      "document": "openai_agents_guide.md",
      "chunk": "The OpenAI Agents SDK provides...",
      "score": "0.85"
    }
  ],
  "session_id": "generated-session-id-or-provided-one"
}
```

Error response (before implementation):
```json
{
  "detail": "TODO: Implement /chat endpoint - this is your Week 1 assignment!"
}
```

## Interactive API Documentation

For interactive testing, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These provide a web UI for testing your API without curl!
