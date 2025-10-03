# Vector Search Tool - Student Assignment

## 📝 Assignment Overview

Complete the implementation of `vector_search_todo.py` by filling in the TODO sections. This assignment will help you understand vector search, Qdrant integration, and building tools for AI agents.

## 🎯 Learning Objectives

By completing this assignment, you will learn:
- How to work with environment variables in Python
- How to connect to and query a vector database (Qdrant)
- How to implement semantic search using FastEmbed
- How to format and structure data for API responses
- How to build error-resilient code with proper exception handling

## 📂 Files

- **`vector_search_todo.py`** - Your assignment file (complete the TODOs)
- **`vector_search.py`** - Reference implementation (check this if stuck)
- **`VECTOR_SEARCH_GUIDE.md`** - Detailed guide with examples for each TODO
- **`../tests/test_vector_search.py`** - Unit tests to verify your implementation

## 🚀 Getting Started

### 1. Set Up Environment Variables
Make sure you have a `.env` file in the project root with:
```
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_api_key
```

### 2. Ensure Data is Loaded
Run the ingestion script to populate the Qdrant collection:
```bash
cd scripts/data_pipeline
uv run python ingest_fed_speeches.py
```

### 3. Read the Guide
Open `VECTOR_SEARCH_GUIDE.md` for detailed instructions and examples.

## ✅ TODO List (8 Items)

### Basic Setup (TODOs 1-4)
- [ ] **TODO 1**: Read environment variables for Qdrant URL and API key
- [ ] **TODO 2**: Validate that credentials are provided
- [ ] **TODO 3**: Initialize Qdrant client
- [ ] **TODO 4**: Set collection name with default value

### Core Functionality (TODOs 5-6)
- [ ] **TODO 5**: Implement vector search using `query_points`
- [ ] **TODO 6**: Format search results into structured dictionaries

### Helper Methods (TODOs 7-8)
- [ ] **TODO 7**: Implement collection verification
- [ ] **TODO 8**: Create user-friendly wrapper function for agents

## 🧪 Testing Your Work

### Run Unit Tests
```bash
cd backend
uv run pytest tests/test_vector_search.py -v
```

**Success criteria:** All 20 tests should pass ✅

### Test Coverage
Check that your code is fully covered:
```bash
uv run pytest tests/test_vector_search.py --cov=tools.vector_search_todo --cov-report=term-missing
```

**Target:** 100% coverage

### Manual Testing
Try your implementation manually:
```bash
cd backend
uv run python test_vector_search_tool.py
```

## 💡 Hints

### Difficulty Level by TODO
- **Easy** (15-30 min): TODOs 1, 2, 4
- **Medium** (30-45 min): TODOs 3, 5, 7
- **Challenging** (45-60 min): TODOs 6, 8

### Common Patterns

**Pattern 1: Environment Variables with Fallback**
```python
value = parameter or os.getenv("ENV_VAR")
```

**Pattern 2: Safe Dictionary Access**
```python
result.payload.get("key", "default_value")
```

**Pattern 3: Error Handling**
```python
try:
    # Try something
    result = risky_operation()
except Exception as e:
    # Handle gracefully
    return {"error": str(e)}
```

## 📚 Resources

- [Qdrant Python Client Docs](https://qdrant.tech/documentation/quick-start/)
- [FastEmbed Documentation](https://qdrant.github.io/fastembed/)
- Reference: `examples/03_qdrant_search.py`
- Solution: `vector_search.py` (only check if truly stuck!)

## 🎓 Assessment Rubric

| Criteria | Points |
|----------|--------|
| All TODOs completed | 40% |
| All unit tests pass | 30% |
| Code follows best practices | 15% |
| Proper error handling | 15% |
| **Total** | **100%** |

## ⏱️ Estimated Time

- **Beginner**: 2-3 hours
- **Intermediate**: 1-2 hours
- **Advanced**: 45-90 minutes

## 🆘 Getting Help

1. **Read the guide**: `VECTOR_SEARCH_GUIDE.md` has detailed examples
2. **Run the tests**: Error messages will guide you
3. **Check the reference**: `vector_search.py` shows the complete solution
4. **Review examples**: `examples/03_qdrant_search.py` demonstrates usage

## 🎉 Completion

Once all tests pass, you've successfully implemented a production-ready vector search tool! This is a key component of RAG (Retrieval-Augmented Generation) systems.

**Next Steps:**
- Integrate this tool with an AI agent
- Experiment with different queries
- Try modifying the search parameters
- Explore other Qdrant features

---

Good luck! 🚀 Remember: it's okay to reference the guide and examples. The goal is to learn, not to struggle in silence.
