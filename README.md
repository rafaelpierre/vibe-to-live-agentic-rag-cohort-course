# 🚀 Production AI Agents - Week 1 Starter Template

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.118.0+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Agents%20SDK-412991.svg)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-DC244C.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Build production-grade AI agents from day one**

[Course Website](https://buildingaiagents.com) • [Documentation](#getting-started) • [Examples](#examples)

</div>

---

## 📖 About This Template

This is the **Week 1 starter template** for the [Production AI Agents Course](https://buildingaiagents.com). You'll build a **Dockerized RAG agent** that queries a knowledge base using OpenAI's Agents SDK and Qdrant vector database.

Unlike typical AI tutorials that stop at Jupyter notebooks, this template teaches you to build **production-ready applications from day one** using Docker, FastAPI, and industry best practices.

### 🎯 What You'll Build

By the end of Week 1, you'll have:
- ✅ A working RAG agent that answers questions from a knowledge base
- ✅ RESTful API powered by FastAPI
- ✅ Fully containerized application with Docker
- ✅ Vector search using Qdrant Cloud
- ✅ Proper error handling and logging
- ✅ Foundation for multi-agent orchestration (Weeks 2-4)

### 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│   FastAPI    │─────▶│   OpenAI    │
│  (Browser)  │      │   Backend    │      │  Agents SDK │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    Qdrant    │
                     │  Vector DB   │
                     └──────────────┘
```

---

## 🗂️ Project Structure

```
production-ai-agents-week1/
├── 📁 app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and environment variables
│   ├── 📁 agents/
│   │   ├── __init__.py
│   │   └── rag_agent.py        # RAG agent implementation (TODO: you build this!)
│   ├── 📁 tools/
│   │   ├── __init__.py
│   │   └── vector_search.py    # Qdrant integration (TODO: you build this!)
│   └── 📁 schemas/
│       ├── __init__.py
│       └── requests.py         # Pydantic models for API requests/responses
│
├── 📁 examples/
│   ├── 01_openai_agents_basics.py       # Learn OpenAI Agents SDK fundamentals
│   ├── 02_qdrant_ingestion.py           # How to ingest documents into Qdrant
│   ├── 03_qdrant_search.py              # How to search vectors in Qdrant
│   ├── 04_docker_basics.md              # Docker crash course
│   └── 05_complete_rag_example.py       # Full RAG flow (reference implementation)
│
├── 📁 data/
│   └── sample_docs/                     # Sample documents for testing
│
├── 📁 scripts/
│   └── setup_qdrant.py                  # Script to populate Qdrant with sample data
│
├── 📁 tests/
│   └── test_api.py                      # Basic API tests
│
├── .env.example                         # Environment variables template
├── .gitignore
├── docker-compose.yml                   # Local development with Docker
├── Dockerfile                           # Production-ready container
├── requirements.txt                     # Python dependencies
└── README.md                            # You are here!
```

---

## 🚀 Getting Started

### Prerequisites

- **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop))
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))
- **Qdrant Cloud account** (free tier) ([Sign up here](https://cloud.qdrant.io/))

No Python installation needed! Docker handles everything.

### Setup (5 Minutes)

1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd production-ai-agents-week1
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Add your API keys to `.env`**
   ```bash
   OPENAI_API_KEY=sk-proj-...
   QDRANT_URL=https://xyz.cloud.qdrant.io
   QDRANT_API_KEY=your-qdrant-key
   ```

4. **Populate Qdrant with sample data** (optional, for testing)
   ```bash
   python scripts/setup_qdrant.py
   ```

5. **Start the application**
   ```bash
   docker-compose up
   ```

6. **Verify it's running**
   - Open your browser: http://localhost:8000
   - API docs: http://localhost:8000/docs

That's it! You're ready to build. 🎉

---

## 📚 Examples

The `examples/` folder contains standalone scripts to help you understand each component:

| Example | Description | Run Time |
|---------|-------------|----------|
| `01_openai_agents_basics.py` | Learn OpenAI Agents SDK fundamentals | 5 mins |
| `02_qdrant_ingestion.py` | Ingest documents into Qdrant vector DB | 10 mins |
| `03_qdrant_search.py` | Perform vector similarity search | 5 mins |
| `04_docker_basics.md` | Docker crash course for beginners | 10 mins |
| `05_complete_rag_example.py` | Full RAG flow reference implementation | 15 mins |

**How to use examples:**

```bash
# Install dependencies locally (if running examples outside Docker)
pip install -r requirements.txt

# Run any example
python examples/01_openai_agents_basics.py
```

💡 **Pro tip**: Start with the examples to understand each piece, then implement your agent in `app/agents/rag_agent.py`.

---

## 🎯 Week 1 Assignment

### Your Mission

Build a **RAG agent** that can answer questions about a knowledge base using:
1. OpenAI Agents SDK for agent orchestration
2. Qdrant for vector search
3. FastAPI for the REST API

### Implementation Checklist

- [ ] **Implement `app/agents/rag_agent.py`**
  - Create an agent using OpenAI Agents SDK
  - Define a tool for searching the knowledge base
  - Handle user queries and generate responses

- [ ] **Implement `app/tools/vector_search.py`**
  - Connect to Qdrant Cloud
  - Implement vector similarity search
  - Return relevant documents with metadata

- [ ] **Create API endpoint in `app/main.py`**
  - `POST /chat` endpoint that accepts a question
  - Call your RAG agent
  - Return the agent's response

- [ ] **Test your agent**
  - Ask questions about the sample knowledge base
  - Verify responses are relevant and accurate
  - Test error handling (invalid queries, API failures)

### Deliverable

Record a **2-3 minute video** showing:
1. Your Docker container running (`docker-compose up`)
2. Making API requests via FastAPI docs or curl
3. Your agent successfully answering questions
4. Brief code walkthrough of your implementation

---

## 🛠️ Development Workflow

### Running the Application

```bash
# Start all services
docker-compose up

# Start in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Making Changes

The `app/` directory is mounted as a volume, so changes you make are reflected immediately (hot reload enabled).

1. Edit code in `app/`
2. Save file
3. FastAPI automatically reloads
4. Test at http://localhost:8000/docs

### Common Commands

```bash
# Rebuild containers after changing dependencies
docker-compose up --build

# Run tests
docker-compose exec app pytest

# Access container shell
docker-compose exec app /bin/bash

# Check Python version
docker-compose exec app python --version
```

---

## 🧪 Testing Your Agent

### Via FastAPI Docs (Recommended)

1. Go to http://localhost:8000/docs
2. Click on `POST /chat`
3. Click "Try it out"
4. Enter your question in the request body
5. Click "Execute"

### Via curl

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the company policy on remote work?"}'
```

### Via Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What is the company policy on remote work?"}
)
print(response.json())
```

---

## 🐛 Troubleshooting

### Docker Issues

**Problem**: `Cannot connect to Docker daemon`
- **Solution**: Make sure Docker Desktop is running

**Problem**: `Port 8000 already in use`
- **Solution**: Stop other services using port 8000, or change the port in `docker-compose.yml`

### API Key Issues

**Problem**: `AuthenticationError: Invalid API key`
- **Solution**: Double-check your `.env` file has the correct keys (no quotes, no spaces)

**Problem**: `Qdrant connection failed`
- **Solution**: Verify your Qdrant Cloud URL and API key are correct

### Agent Issues

**Problem**: Agent returns irrelevant answers
- **Solution**: Check your vector search implementation - are you retrieving the right documents?

**Problem**: Agent takes too long to respond
- **Solution**: Limit the number of documents retrieved (try top_k=3 instead of 10)

---

## 📖 Learning Resources

### OpenAI Agents SDK
- [Official Documentation](https://platform.openai.com/docs/assistants/overview)
- [Cookbook Examples](https://cookbook.openai.com/)

### Qdrant Vector Database
- [Getting Started Guide](https://qdrant.tech/documentation/quick-start/)
- [Python Client Docs](https://python-client.qdrant.tech/)

### FastAPI
- [Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Best Practices](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

### Docker
- [Docker Crash Course](./examples/04_docker_basics.md) (included in this repo)
- [Official Documentation](https://docs.docker.com/)

---

## 🎓 Next Steps

After completing Week 1:

- **Week 2**: Multi-agent orchestration with specialized agents (router, retrieval, synthesis)
- **Week 3**: Deploy to Azure with observability and guardrails
- **Week 4**: Build your own production-grade agent (capstone project)

Want to learn more? [Join the full course at buildingaiagents.com](https://buildingaiagents.com)

---

## 🤝 Getting Help

### During the Course

- **Slack Community**: Ask questions, share progress, get help from peers and instructors
- **1-on-1 Sessions**: Schedule 30-minute sessions with the instructor (Rafael Pierre)
- **Office Hours**: Weekly live sessions for Q&A

### Self-Study

- Check the `examples/` folder for reference implementations
- Review the troubleshooting section above
- Open an issue in this repository

---

## 📝 License

MIT License - feel free to use this template for learning and building your own projects!

---

## 🌟 About the Course

This template is part of **[From Vibe to Live: Build and Deploy Production AI Agents](https://buildingaiagents.com)**, a 4-week cohort-based course where you learn to:

- ✨ Build multi-agent systems with OpenAI Agents SDK
- 🚀 Deploy to Azure with Docker and FastAPI
- 📊 Implement observability with Phoenix Arize
- 🛡️ Add guardrails for security and reliability
- 💼 Create portfolio-ready projects

**Taught by Rafael Pierre** - 17+ years in Software Engineering, Data and AI, ex-Hugging Face, Databricks

[**Enroll now at buildingaiagents.com** →](https://buildingaiagents.com)

---

<div align="center">

**Built with ❤️ for production AI**

[Course](https://buildingaiagents.com) • [Examples](#examples) • [Troubleshooting](#troubleshooting)

</div>
