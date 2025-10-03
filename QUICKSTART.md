# Quick Start Guide

Get up and running with the Agentic RAG course project in 5 minutes!

## Prerequisites

- GitHub account (for Codespaces)
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Qdrant Cloud account ([free tier](https://qdrant.tech/))

## Step 1: Open in GitHub Codespaces

Click the "Code" button on this repository and select "Open with Codespaces" → "New codespace"

The dev container will automatically:
- Install Python 3.11 and uv
- Set up Docker-in-Docker
- Install VS Code extensions
- Run `cd backend && uv sync` to install dependencies

Wait for the container to finish building (2-3 minutes).

## Step 2: Configure Environment Variables

1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```bash
   code .env
   ```

   Required values:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `QDRANT_URL`: Your Qdrant Cloud URL (e.g., `https://xxx.qdrant.io`)
   - `QDRANT_API_KEY`: Your Qdrant API key

## Step 3: Set Up Qdrant with Data

You have two options for populating your knowledge base:

### Option A: Sample Documents (Quick Start)

Run the setup script to populate your Qdrant collection with curated sample documents:

```bash
cd backend
uv run python ../scripts/data_pipeline/setup_qdrant.py
```

This will:
- Load 6 sample documents about AI, RAG, Qdrant, FastAPI, and Docker
- Generate embeddings using OpenAI
- Create a Qdrant collection
- Upload the documents

### Option B: Federal Reserve Speeches (Real-World Data)

For a more realistic dataset, scrape recent Federal Reserve speeches:

```bash
cd scripts/data_pipeline

# Fetch all speeches from the RSS feed
uv run python fetch_fed_speeches.py

# Ingest into Qdrant
cd ../../backend
uv run python ../scripts/data_pipeline/ingest_fed_speeches.py
```

This provides:
- **15+ real speeches** from Federal Reserve officials
- Current economic and monetary policy content
- Realistic document lengths and complexity
- Better test queries: "What is the Fed's outlook on inflation?" or "Summarize recent monetary policy discussions"

**Recommended:** Use Option B for a more challenging and realistic RAG experience!

## Step 4: Explore the Examples

Before implementing the assignment, explore the examples:

```bash
# Example 1: OpenAI Agents SDK basics
uv run python ../examples/01_openai_agents_basics.py

# Example 2: Qdrant document ingestion
uv run python ../examples/02_qdrant_ingestion.py

# Example 3: Vector search
uv run python ../examples/03_qdrant_search.py

# Example 5: Complete RAG reference (don't copy directly!)
uv run python ../examples/05_complete_rag_example.py
```

Read `examples/04_docker_basics.md` for Docker concepts.

## Step 5: Understand the Assignment

Your Week 1 assignment is to implement the RAG agent by completing TODOs in:

1. **`backend/src/tools/vector_search.py`**
   - Initialize Qdrant and OpenAI clients
   - Implement embedding generation
   - Implement vector search
   - Implement the tool function

2. **`backend/src/agents/rag_agent.py`**
   - Initialize OpenAI client
   - Set up the agent with instructions and tools
   - Implement the chat method

3. **`backend/src/main.py`**
   - Initialize the RAG agent on startup
   - Implement the `/chat` endpoint

## Step 6: Implement Your Solution

Open the files listed above and look for `TODO` comments. Each file has:
- Detailed docstrings explaining what each method should do
- Hints about which APIs to use
- Clear structure to guide implementation

Tips:
- Start with `vector_search.py` (the tool)
- Then implement `rag_agent.py` (the agent)
- Finally, wire it up in `main.py` (the API)
- Use the examples as reference (but don't copy directly!)

## Step 7: Test Your Implementation

### Run the API locally

```bash
cd backend
uv run uvicorn src.main:app --reload
```

### Test endpoints

```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the OpenAI Agents SDK?"}'
```

### Use interactive docs

Open http://localhost:8000/docs in your browser for interactive API testing.

## Step 8: Test with Docker

```bash
# Build and run
docker-compose up

# In another terminal, test
curl http://localhost:8000/health
```

## Success Criteria

Your implementation is complete when:

- ✅ The API starts without errors
- ✅ `/health` endpoint returns `{"status": "healthy"}`
- ✅ `/chat` endpoint accepts queries and returns answers
- ✅ Answers are based on retrieved documents (not just generic responses)
- ✅ The agent uses the search tool automatically
- ✅ Everything works in Docker

## Troubleshooting

### Dependencies not installed

```bash
cd backend
uv sync
```

### Environment variables not loaded

Make sure `.env` is in the **project root**, not in `backend/`.

### Qdrant connection failed

1. Check your `QDRANT_URL` and `QDRANT_API_KEY`
2. Make sure you've created a cluster in Qdrant Cloud
3. Run the setup script again

### Import errors in VS Code

VS Code should auto-detect the virtual environment. If not:
1. Press `Cmd/Ctrl + Shift + P`
2. Type "Python: Select Interpreter"
3. Choose the `.venv` interpreter

### Docker build fails

```bash
# Clean and rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## Next Steps

After completing Week 1:
- Week 2: Testing, monitoring, and observability
- Week 3: Advanced RAG (reranking, hybrid search, citations)
- Week 4: Production deployment with CI/CD

## Getting Help

- Read the detailed README.md
- Check `backend/README.md` for backend-specific info
- Review the examples in `examples/`
- Look at example 5 for a complete reference implementation

Good luck! 🚀
