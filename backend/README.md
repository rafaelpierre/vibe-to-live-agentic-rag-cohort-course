# Backend - Agentic RAG API

Production-ready FastAPI backend for the Agentic RAG course project.

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with /chat endpoint (TODO)
│   ├── config.py            # Settings management with pydantic-settings
│   ├── agents/
│   │   ├── __init__.py
│   │   └── rag_agent.py     # RAG agent implementation (TODO)
│   ├── tools/
│   │   ├── __init__.py
│   │   └── vector_search.py # Qdrant vector search tool (TODO)
│   └── schemas/
│       ├── __init__.py
│       └── requests.py      # Pydantic request/response models
├── tests/                   # Unit tests (to be added)
├── pyproject.toml           # Dependencies and project metadata
└── README.md                # This file
```

## Week 1 Assignment: Implement the RAG Agent

Your task is to complete the TODO sections in the following files:

### 1. `src/tools/vector_search.py`

Implement the `VectorSearchTool` class:
- [ ] Initialize Qdrant and OpenAI clients in `__init__()`
- [ ] Implement `_generate_embedding()` to create embeddings
- [ ] Implement `search()` to perform vector similarity search
- [ ] Implement `search_knowledge_base()` tool function

### 2. `src/agents/rag_agent.py`

Implement the `RAGAgent` class:
- [ ] Initialize OpenAI client in `__init__()`
- [ ] Set up the agent with instructions and tools in `_setup_agent()`
- [ ] Implement `chat()` method to handle user queries
- [ ] (Optional) Implement `_extract_sources()` for transparency

### 3. `src/main.py`

Complete the FastAPI application:
- [ ] Initialize RAG agent in `startup_event()`
- [ ] Implement `/chat` endpoint to process user queries
- [ ] Handle errors appropriately

## Setup

### 1. Install Dependencies

```bash
cd backend
uv sync
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp ../.env.example ../.env
```

Required variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: Your Qdrant Cloud URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_COLLECTION_NAME`: Collection name (default: `course_documents`)

### 3. Populate Qdrant with Sample Data

```bash
uv run python ../scripts/setup_qdrant.py
```

This script will:
- Load sample documents from `data/sample_docs/`
- Generate embeddings using OpenAI
- Create a Qdrant collection
- Upload documents to Qdrant

## Running the Application

### Development Mode (with auto-reload)

```bash
uv run uvicorn src.main:app --reload
```

### Production Mode (with Docker)

```bash
cd ..
docker-compose up
```

## Testing Your Implementation

### 1. Health Check

```bash
curl http://localhost:8000/health
```

### 2. Interactive API Docs

Open your browser to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Test the Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the OpenAI Agents SDK?"}'
```

Expected response:
```json
{
  "answer": "The OpenAI Agents SDK is...",
  "sources": [...],
  "session_id": "..."
}
```

## Learning Resources

### Examples

Check the `examples/` directory for:
1. `01_openai_agents_basics.py` - OpenAI Agents SDK introduction
2. `02_qdrant_ingestion.py` - Document ingestion
3. `03_qdrant_search.py` - Vector search examples
4. `04_docker_basics.md` - Docker cheatsheet
5. `05_complete_rag_example.py` - Complete RAG reference implementation

### Documentation

- [OpenAI Agents SDK](https://platform.openai.com/docs/assistants/overview)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Code Quality

### Linting and Formatting

```bash
# Check code with ruff
uv run ruff check .

# Format code with ruff
uv run ruff format .
```

### Testing (to be implemented in Week 2)

```bash
uv run pytest
```

## Troubleshooting

### Import Errors

If you see import errors in VS Code:
1. Make sure you've run `uv sync`
2. VS Code should auto-detect the virtual environment
3. If not, run: Command Palette → Python: Select Interpreter

### Environment Variables Not Loading

Make sure your `.env` file is in the project root (not in `backend/`).

### Qdrant Connection Issues

1. Verify your `QDRANT_URL` and `QDRANT_API_KEY` are correct
2. Check that you've created a Qdrant Cloud account and cluster
3. Run the setup script to create the collection

### Docker Issues

```bash
# Rebuild the image
docker-compose build

# View logs
docker-compose logs -f

# Reset everything
docker-compose down -v
```

## Week 1 Success Criteria

Your implementation should:
- ✅ Successfully start the FastAPI server
- ✅ Respond to health check at `/health`
- ✅ Accept POST requests to `/chat` with a query
- ✅ Search Qdrant for relevant documents
- ✅ Generate responses using OpenAI Agents SDK
- ✅ Return structured responses with answer and sources
- ✅ Handle errors gracefully
- ✅ Run successfully in Docker

## Next Steps

After completing Week 1:
- Week 2: Add comprehensive testing and monitoring
- Week 3: Implement advanced RAG features (reranking, hybrid search)
- Week 4: Deploy to production with CI/CD

Good luck! 🚀
