"""
Example 05: Complete RAG Implementation

This is a REFERENCE IMPLEMENTATION showing how all the pieces fit together.
Students should NOT copy this directly - it's meant as a guide for understanding.

This example shows:
1. Complete RAG agent implementation
2. Integration with OpenAI Agents SDK
3. Vector search tool integration
4. Proper error handling and logging

For Week 1 assignment, students should implement this in the backend/src/ structure.
"""

import os

from openai import OpenAI
from openai.agents import Agent
from qdrant_client import QdrantClient


class CompleteTool:
    """Complete vector search tool implementation (REFERENCE ONLY)."""

    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "course_documents")

    def _generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for text."""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search for relevant documents."""
        # Generate query embedding
        query_vector = self._generate_embedding(query)

        # Search Qdrant
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append(
                {
                    "content": result.payload.get("content", ""),
                    "metadata": {
                        "source": result.payload.get("source", "unknown"),
                        "topic": result.payload.get("topic", "unknown"),
                        "page": result.payload.get("page", 0),
                    },
                    "score": float(result.score),
                }
            )

        return formatted_results


# Global tool instance
_tool = None


def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant information.

    This function is used as a tool by the OpenAI agent.
    """
    global _tool
    if _tool is None:
        _tool = CompleteTool()

    results = _tool.search(query, limit=3)

    # Format results as a readable string
    formatted_output = "Found the following relevant information:\n\n"

    for i, result in enumerate(results, 1):
        formatted_output += f"Result {i} (relevance: {result['score']:.2f}):\n"
        formatted_output += f"Source: {result['metadata']['source']}\n"
        formatted_output += f"Content: {result['content']}\n\n"

    return formatted_output


class CompleteRAGAgent:
    """Complete RAG agent implementation (REFERENCE ONLY)."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._setup_agent()

    def _setup_agent(self):
        """Set up the agent with instructions and tools."""
        self.agent = Agent(
            name="RAG Assistant",
            instructions="""
            You are a helpful AI assistant with access to a knowledge base about AI development,
            agents, RAG, vector databases, FastAPI, and Docker.
            
            When answering questions:
            1. Use the search_knowledge_base tool to find relevant information
            2. Synthesize information from multiple sources if needed
            3. Cite your sources when providing information
            4. If the knowledge base doesn't contain relevant information, say so clearly
            5. Be concise but comprehensive
            
            Always strive to provide accurate, helpful responses based on the knowledge base.
            """,
            tools=[search_knowledge_base],
            model="gpt-4o-mini",
        )

    def chat(self, query: str, thread_id: str | None = None) -> dict:
        """
        Process a user query.

        Args:
            query: User's question
            thread_id: Optional thread ID for conversation continuity

        Returns:
            Dictionary with answer, sources, and thread_id
        """
        # Create or use existing thread
        if thread_id is None:
            thread = self.client.beta.threads.create()
            thread_id = thread.id

        # Add user message
        self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=query
        )

        # Run agent
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.agent.id,
        )

        # Get response
        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            answer = messages.data[0].content[0].text.value

            # Extract sources from tool calls if available
            sources = self._extract_sources(run)

            return {
                "answer": answer,
                "sources": sources,
                "thread_id": thread_id,
            }
        else:
            raise Exception(f"Agent run failed with status: {run.status}")

    def _extract_sources(self, run) -> list[dict] | None:
        """Extract sources from agent tool calls."""
        # This would parse the run object to find tool calls
        # and extract source information from search results
        # For simplicity, returning None here
        return None


def main():
    """Run the complete RAG example."""
    print("🤖 Complete RAG Implementation Example")
    print("=" * 50)
    print("\n⚠️  This is a REFERENCE implementation for learning.")
    print("Students should implement this in backend/src/ for the assignment.\n")

    # Check for required environment variables
    required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(
            f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}"
        )
        print("Please set them in your .env file")
        exit(1)

    # Create RAG agent
    print("1️⃣ Initializing RAG agent...")
    agent = CompleteRAGAgent()
    print("   ✅ Agent initialized\n")

    # Test queries
    queries = [
        "What is the OpenAI Agents SDK?",
        "How does RAG work?",
        "Tell me about vector databases and Qdrant",
    ]

    print("2️⃣ Running test queries...\n")

    for i, query in enumerate(queries, 1):
        print(f"{'=' * 50}")
        print(f"Query {i}: {query}")
        print(f"{'=' * 50}\n")

        try:
            result = agent.chat(query)
            print(f"Answer: {result['answer']}\n")

            if result.get("sources"):
                print("Sources:")
                for source in result["sources"]:
                    print(f"  - {source}")

            print()
        except Exception as e:
            print(f"❌ Error: {e}\n")

    print("✅ Example complete!")
    print("\n💡 Key Implementation Points:")
    print("   1. Tool initialization happens once and is reused")
    print("   2. Agent maintains conversation context via threads")
    print("   3. Error handling ensures graceful failures")
    print("   4. Sources provide transparency and traceability")
    print("   5. The agent decides when to use the search tool")
    print("\n📝 For Week 1 Assignment:")
    print("   - Implement VectorSearchTool in backend/src/tools/vector_search.py")
    print("   - Implement RAGAgent in backend/src/agents/rag_agent.py")
    print("   - Complete the /chat endpoint in backend/src/main.py")
    print("   - Test with Docker: docker-compose up")


if __name__ == "__main__":
    main()
