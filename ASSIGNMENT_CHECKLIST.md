# Week 1 Assignment Checklist

Use this checklist to track your progress on the Week 1 assignment.

## Prerequisites ✅

- [ ] Created OpenAI account and got API key
- [ ] Created Qdrant Cloud account and cluster
- [ ] Opened project in GitHub Codespaces (or local dev container)
- [ ] Copied `.env.example` to `.env` and filled in credentials
- [ ] Ran setup script: `cd backend && uv run python ../scripts/setup_qdrant.py`

## Learning Phase 📚

- [ ] Read the main README.md
- [ ] Read `backend/README.md`
- [ ] Ran `examples/01_openai_agents_hello_world.py` and understood the code
- [ ] Ran `examples/02_qdrant_ingestion.py` and understood the code

## Implementation Phase 🔨

### File 1: `backend/src/tools/vector_search.py`

- [ ] Implemented `VectorSearchTool.__init__()`
  - [ ] Initialized `self.qdrant_client` with URL and API key
  - [ ] Initialized `self.openai_client` with API key
  
- [ ] Implemented `VectorSearchTool._generate_embedding()`
  - [ ] Called OpenAI embeddings API
  - [ ] Used `text-embedding-3-small` model
  - [ ] Returned embedding as list of floats
  
- [ ] Implemented `VectorSearchTool.search()`
  - [ ] Generated embedding for query
  - [ ] Called Qdrant search API
  - [ ] Formatted results with content, metadata, and score
  - [ ] Returned list of result dictionaries
  
- [ ] Implemented `search_knowledge_base()` function
  - [ ] Created VectorSearchTool instance
  - [ ] Called search method
  - [ ] Formatted results as readable string
  - [ ] Returned string for agent to use

### File 2: `backend/src/agents/rag_agent.py`

- [ ] Implemented `RAGAgent.__init__()`
  - [ ] Initialized `self.client` with OpenAI API key
  - [ ] Called `_setup_agent()`
  
- [ ] Implemented `RAGAgent._setup_agent()`
  - [ ] Created Agent with appropriate name
  - [ ] Wrote clear instructions for the agent
  - [ ] Registered `search_knowledge_base` tool
  - [ ] Set model from settings
  
- [ ] Implemented `RAGAgent.chat()`
  - [ ] Created or retrieved thread using session_id
  - [ ] Added user message to thread
  - [ ] Ran agent with `create_and_poll()`
  - [ ] Extracted response from messages
  - [ ] Returned dictionary with answer and session_id
  
- [ ] (Optional) Implemented `RAGAgent._extract_sources()`
  - [ ] Parsed tool calls from run object
  - [ ] Extracted source information
  - [ ] Returned list of source dictionaries

### File 3: `backend/src/main.py`

- [ ] Implemented `startup_event()`
  - [ ] Used `create_rag_agent()` to initialize agent
  - [ ] Assigned to global `rag_agent` variable
  
- [ ] Implemented `/chat` endpoint
  - [ ] Called `rag_agent.chat()` with query and session_id
  - [ ] Created ChatResponse from result
  - [ ] Added try/except for error handling
  - [ ] Returned proper HTTP status codes

## Testing Phase 🧪

### Manual Testing

- [ ] Started API with: `cd backend && uv run uvicorn src.main:app --reload`
- [ ] Tested `/health` endpoint: `curl http://localhost:8000/health`
- [ ] Tested root endpoint: `curl http://localhost:8000/`
- [ ] Tested `/chat` endpoint with simple query
- [ ] Tested `/chat` with session_id
- [ ] Verified answers are relevant to queries
- [ ] Checked that sources are included (if implemented)
- [ ] Opened http://localhost:8000/docs and tested interactively

### Example Queries to Test

- [ ] "What is the OpenAI Agents SDK?"
- [ ] "How does RAG work?"
- [ ] "What are the benefits of using Qdrant?"
- [ ] "Why should I use FastAPI for AI applications?"
- [ ] "What are Docker best practices?"
- [ ] "Tell me about production AI considerations"

### Docker Testing

- [ ] Built Docker image: `docker-compose build`
- [ ] Started container: `docker-compose up`
- [ ] Verified health check: `curl http://localhost:8000/health`
- [ ] Tested chat endpoint through Docker
- [ ] Checked logs: `docker-compose logs -f`
- [ ] Stopped cleanly: `docker-compose down`

## Code Quality 🎨

- [ ] Ran linter: `cd backend && uv run ruff check .`
- [ ] Fixed any linting issues
- [ ] Ran formatter: `uv run ruff format .`
- [ ] Added type hints where appropriate
- [ ] Added docstrings for custom methods
- [ ] Removed debug print statements

## Documentation 📝

- [ ] Updated any comments if I changed the approach
- [ ] Verified all TODOs are removed or addressed
- [ ] Could explain each part of my implementation to someone else

## Bonus Points 🌟 (Optional)

- [ ] Implemented `_extract_sources()` for transparency
- [ ] Added custom error messages for different failure modes
- [ ] Added request logging to track queries
- [ ] Experimented with different agent instructions
- [ ] Tried different embedding models or search parameters
- [ ] Added pagination or filtering to search results
- [ ] Created additional test queries
- [ ] Documented edge cases I discovered

## Final Checklist ✅

- [ ] All endpoints return expected responses
- [ ] Answers are grounded in retrieved documents
- [ ] Application runs without errors
- [ ] Docker build and run successfully
- [ ] Code is clean and well-organized
- [ ] Ready to demo to instructor/peers

## Submission 🚀

- [ ] Committed all changes to git
- [ ] Pushed to GitHub repository
- [ ] Created PR from `feature/week1` to `main` (if using branches)
- [ ] Added screenshots or screen recording to submission
- [ ] Wrote summary of implementation approach
- [ ] Listed any challenges encountered and solutions

---

**Estimated Time:** 4-6 hours

**Tips:**
- Start with the vector search tool - it's the foundation
- Test each component individually before moving to the next
- Use the examples as reference, but understand the code
- Don't hesitate to experiment and learn from errors
- The goal is learning, not perfection!

Good luck! 🎓
