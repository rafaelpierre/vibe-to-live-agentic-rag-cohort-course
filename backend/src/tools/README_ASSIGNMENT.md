# Vector Search Tool - Student Assignment

## 📝 Assignment Overview

Complete the implementation of `vector_search.py` by filling in the TODO sections. This assignment will help you understand vector search, Qdrant integration, and building tools for AI agents.

## 🎯 Learning Objectives

By completing this assignment, you will learn:
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

### Ensure Data is Loaded
Run the ingestion script to populate the Qdrant collection:
```bash
cd scripts/data_pipeline
uv run python ingest_fed_speeches.py
```

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

**Success criteria:** Ideally, all 20 tests should pass ✅

## 💡 Hints

### Difficulty Level by TODO
- **Easy** (15-30 min): TODOs 1, 2, 4
- **Medium** (30-45 min): TODOs 3, 5, 7
- **Challenging** (45-60 min): TODOs 6, 8


## 📚 Resources

- [Qdrant Python Client Docs](https://qdrant.tech/documentation/quick-start/)
- [FastEmbed Documentation](https://qdrant.github.io/fastembed/)
- Reference: `scripts/data_pipeline/ingest_fed_speeches.py`

## 🎓 Assessment Rubric

| Criteria | Points |
|----------|--------|
| All TODOs completed | 50% |
| All unit tests pass | 35% |
| Code follows best practices | 15% |
| **Total** | **100%** |

## ⏱️ Estimated Time

- **Beginner**: 2-3 hours
- **Intermediate**: 1-2 hours
- **Advanced**: 45-90 minutes

## 🆘 Getting Help

1. **Run the tests**: Error messages will guide you
2. **Review the ingestion script**: `scripts/data_pipeline/ingest_fed_speeches.py` demonstrates usage

## 🎉 Completion

Once all tests pass, you've successfully implemented a production-ready vector search tool! This is a key component of RAG (Retrieval-Augmented Generation) systems.

**Next Steps:**
- Integrate this tool with an AI agent
- Experiment with different queries
- Try modifying the search parameters
- Explore other Qdrant features

---

Good luck! 🚀 Remember: it's okay to reference the guide and examples. The goal is to learn, not to struggle in silence.
