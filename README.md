# 🚀 From Vibe to Live: Build and Deploy Production AI Agents

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-Agents%20SDK-412991?style=for-the-badge&logo=openai&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Cloud-DC244C?style=for-the-badge&logo=qdrant&logoColor=white)
![Phoenix](https://img.shields.io/badge/Phoenix-Arize-FF6B35?style=for-the-badge&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Build production-grade AI agents from day one**

[Course Website](https://buildingaiagents.com) • [Week 1](#week-1-rag-agent-foundations) • [Week 2](#week-2-multi-agent-orchestration) • [Week 3](#week-3-production-deployment) • [Week 4](#week-4-capstone)

</div>

---

## 📖 About This Repository

This is the **official code repository** for the [From Vibe to Live: Production AI Agents Course](https://buildingaiagents.com). 

Each week builds incrementally on the previous, culminating in a **production-deployed AI agent** with observability, guardrails, and enterprise-grade architecture.

### 🗂️ Repository Structure

This repo uses **branches for each week**:

- **`feature/week1`** → RAG Agent Foundations
- **`feature/week2`** → Multi-Agent Orchestration
- **`feature/week3`** → Production Deployment + Observability
- **`feature/week4`** → Capstone Project Templates

**To switch weeks:**
```bash
git checkout feature/week1    # Start with foundations
git checkout feature/week2    # Move to orchestration
git checkout feature/week3    # Deploy to production
git checkout feature/week4    # Build your capstone
```

---

## 🎯 Weekly Learning Path

### Week 1: RAG Agent Foundations
**Branch:** `feature/week1`

Build a Dockerized RAG agent that queries a knowledge base.

**What you'll build:**
- ✅ Single RAG agent with vector search
- ✅ FastAPI REST API
- ✅ Fully containerized with Docker
- ✅ Qdrant Cloud integration

---

### Week 2: Multi-Agent Orchestration
**Branch:** `feature/week2`

Extend your agent into a multi-agent system with specialized roles.

**What you'll add:**
- Router agent (intent classification)
- Retrieval agent (vector search specialist)
- Synthesis agent (response generation)
- Multi-tool coordination
- Basic Observability with Phoenix Arize

---

### Week 3: Production Deployment + Observability
**Branch:** `feature/week3`

Deploy to Azure with full observability and guardrails.

**What you'll add:**
- Azure Container Apps deployment
- Advanced Observability (LLM as a Judge, Trajectory Evaluation)
- Prompt injection detection
- Response validation guardrails
- Cost tracking and monitoring

---

### Week 4: Capstone Project
**Branch:** `feature/week4`

Build your own production-grade agent with advanced features.

**Options:**
- Enhanced enterprise assistant with memory
- Domain-specific agent (legal, medical, code)
- Advanced multi-agent workflows
- CI/CD pipeline with GitHub Actions

---

### 🏗️ Architecture Evolution

**Week 1 - Simple RAG Agent:**

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#0EA5E9','primaryTextColor':'#fff','primaryBorderColor':'#0284C7','lineColor':'#64748B','secondaryColor':'#8B5CF6','tertiaryColor':'#10B981'}}}%%
graph TD
    A["🌐 Client<br/>Browser"] -->|"📤 HTTP Request"| B["⚡ FastAPI<br/>Backend"]
    B -->|"🔗 Exposes"| C["🤖 OpenAI<br/>Agents SDK"]
    C -->|"🔍 Vector Search"| D["💾 Qdrant<br/>Vector DB"]
    C -->|"💬 LLM Calls"| E["✨ GPT-4o"]
    
    style A fill:#0EA5E9,stroke:#0284C7,stroke-width:3px,color:#fff
    style B fill:#10B981,stroke:#059669,stroke-width:3px,color:#fff
    style C fill:#8B5CF6,stroke:#7C3AED,stroke-width:3px,color:#fff
    style D fill:#DC2626,stroke:#B91C1C,stroke-width:3px,color:#fff
    style E fill:#F59E0B,stroke:#D97706,stroke-width:3px,color:#fff
    
    linkStyle 0 stroke:#0EA5E9,stroke-width:2px
    linkStyle 1 stroke:#10B981,stroke-width:2px
    linkStyle 2 stroke:#DC2626,stroke-width:2px
    linkStyle 3 stroke:#F59E0B,stroke-width:2px
```

**Week 2** adds multiple specialized agents (Router, Retrieval, Synthesis)  
**Week 3** adds observability layer (Phoenix Arize), guardrails, and Azure deployment  
**Week 4** showcases advanced patterns based on your capstone project

---

## 🗂️ Project Structure

The repository structure evolves each week as you add more capabilities:

**Week 1:**
```
production-ai-agents/
├── 📁 src/                      # Core application code
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Configuration
│   ├── 📁 agents/               # Agent implementations
│   └── 📁 tools/                # Agent tools (vector search, etc.)
├── 📁 examples/                 # Learning examples
├── 📁 data/                     # Sample documents
├── 📁 scripts/                  # Setup and utility scripts
└── 📁 tests/                    # Tests
```

**Week 2** adds:
- Multi-agent orchestration patterns
- `src/agents/router_agent.py` - Intent classification
- `src/agents/synthesis_agent.py` - Response generation
- `src/observability/` - Phoenix Arize integration

**Week 3** adds:
- `src/guardrails/` - Security and validation
- `.github/workflows/` - CI/CD pipelines
- Azure deployment configurations

**Week 4** varies:
- Custom agents based on your capstone project
- Advanced features (memory, caching, etc.)

> **View full structure:** Check each branch to see how the project evolves.

---

## 🚀 Getting Started

### Prerequisites
#### GitHub Codespaces

Work directly in your browser or your favorite IDE with zero local setup!

- **What it is**: A complete dev environment in the cloud with Docker, Python, and all dependencies pre-installed
- **Why use it**: No local installation needed, works on any device, consistent environment for all students
- **IDE support**: Works seamlessly with VS Code (web or desktop) and Cursor
- **Free tier**: 60 hours/month for free on GitHub

**How to use:**
1. Click the **Code** button on the GitHub repo
2. Select **Codespaces** tab
3. Click **Create codespace on week1** (or current branch)
4. Wait ~2 minutes for the devcontainer to build
5. Start coding! All dependencies are already installed

[📖 Learn more about GitHub Codespaces](https://docs.github.com/en/codespaces/overview)

> **Pro tip**: You can open your Codespace in VS Code Desktop or Cursor by clicking the menu (three lines) → "Open in..." → "VS Code Desktop" or use the Cursor extension.

### Setup (5 Minutes)

1. **Create a Codespace**
   - Click **Code** → **Codespaces** → **Create codespace on week1**
   - Wait for devcontainer to build (~2 minutes)

2. Add your API keys as Codespace Secret Variables

4. **Populate Qdrant with sample data**
   ```bash
   python scripts/data_pipeline/ingest_fed_speeches.py
   ```

---

## 📚 Learning Resources

### Examples (Week 1+)

The `examples/` folder contains standalone scripts to help you understand each component

**How to use examples:**

```bash
# Install dependencies locally (if running examples outside Docker)
# With uv (recommended)
uv sync

# Run any example
uv run python examples/01_openai_agents_hello_world.py
```

💡 **Pro tip**: Start with the examples to understand each piece, then implement your solution in the `src/` directory.

### Documentation Links

**OpenAI Agents SDK**
- [Official Documentation](https://openai.github.io/openai-agents-python/)
- [Cookbook Examples](https://github.com/openai/openai-agents-python/tree/main/examples)

**Qdrant Vector Database**
- [Getting Started Guide](https://qdrant.tech/documentation/quick-start/)
- [Python Client Docs](https://python-client.qdrant.tech/)

**FastAPI**
- [Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Best Practices](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

**Docker**
- [Docker Crash Course](./examples/04_docker_basics.md) (included in this repo)
- [Official Documentation](https://docs.docker.com/)

---

## 🎯 Current Week Assignment

> **Note:** Assignment details vary by branch. Switch to the appropriate week's branch to see specific requirements.

### Week 1 Assignment: Build a RAG Agent

**Your Mission:**

Build a **RAG agent** that can answer questions about a knowledge base using:
1. OpenAI Agents SDK for agent orchestration
2. Qdrant for vector search
3. FastAPI for the REST API

---

## 🎓 What's Next?

After completing each week, advance to the next branch:

```bash
# Completed Week 1? Move to Week 2:
git checkout week2

# Completed Week 2? Move to Week 3:
git checkout week3

# Ready for your capstone?
git checkout week4
```

Each week builds on the previous, so make sure to complete assignments in order!

**Want the full experience?** [Join the course at buildingaiagents.com](https://buildingaiagents.com) for:
- Live instruction and Q&A sessions
- 1-on-1 mentorship with Rafael Pierre
- Slack community support
- $400 in free OpenAI credits
- Certificate of completion

---

## 🤝 Getting Help

### During the Course

- **Slack Community**: Ask questions, share progress, get help from peers and instructors
- **1-on-1 Sessions**: Schedule 30-minute sessions with the instructor (Rafael)

### Self-Study

- Check the `examples/` folder for reference implementations
- Review the troubleshooting section above
- Open an issue in this repository

---

## Appendix: Syncing your branch with the assignment repo

To sync your fork branch (e.g. `feature/week1-rafael`) with the original repo's branch `feature/week1`, follow these steps:

* Make sure you have the original repo added as the upstream remote (Only do this once if not already added):

```
git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPO.git
```

* Fetch the latest changes from the original repo:

```
git fetch upstream
```

* Checkout your branch locally:

```
git checkout feature/week1-rafael
```

* Merge or rebase the changes from the original branch into your branch:

```
git merge upstream/feature/week1
```

* Push the updated branch to your forked repo:

```
git push origin feature/week1-rafael
```

This keeps your `feature/week1-rafael` branch synced with the original `feature/week1` branch from the upstream repo.

## 📝 License

MIT License - feel free to use this template for learning and building your own projects!

---

## 🌟 About the Course

This repository is part of **[From Vibe to Live: Build and Deploy Production AI Agents](https://buildingaiagents.com)**, a 4-week cohort-based course where you learn to:

- ✨ Build multi-agent systems with OpenAI Agents SDK
- 🚀 Deploy to Azure with Docker and FastAPI
- 📊 Implement observability with Phoenix Arize
- 🛡️ Add guardrails for security and reliability
- 💼 Create portfolio-ready projects

**Taught by [Rafael Pierre](https://www.linkedin.com/in/rafaelpierre)** - 17+ years in Software Engineering, Data and AI, ex-Hugging Face, Databricks

[**Enroll now at buildingaiagents.com** →](https://buildingaiagents.com)

---

<div align="center">

**Built with ❤️ for production AI**

[Course](https://buildingaiagents.com) • [Examples](#learning-resources) • [Troubleshooting](#troubleshooting)

</div>
