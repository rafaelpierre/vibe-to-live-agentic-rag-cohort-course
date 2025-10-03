"""
RAG (Retrieval-Augmented Generation) Agent using OpenAI Agents SDK.
"""

from openai import OpenAI
from openai.agents import Agent

from ..config import settings
from ..tools.vector_search import search_knowledge_base


class RAGAgent:
    """
    An agentic RAG implementation using OpenAI Agents SDK.

    This agent can:
    - Search a knowledge base using vector similarity
    - Reason about which information is relevant
    - Generate informed responses based on retrieved context
    - Handle multi-turn conversations
    """

    def __init__(self):
        """Initialize the RAG agent with OpenAI client and tools."""
        # TODO: Initialize OpenAI client
        # Hint: Use OpenAI() with api_key from settings
        self.client = None

        # TODO: Create the agent with appropriate configuration
        # Hint: Use Agent() with model, instructions, and tools
        self.agent = None

        self._setup_agent()

    def _setup_agent(self):
        """
        Configure the agent with instructions and tools.

        TODO: Implement this method
        Key considerations:
        1. Define clear instructions for the agent
        2. Register the search_knowledge_base tool
        3. Configure appropriate model parameters
        """
        # TODO: Set up the agent
        # Example structure:
        # self.agent = Agent(
        #     name="RAG Assistant",
        #     instructions="You are a helpful assistant that...",
        #     tools=[search_knowledge_base],
        #     model=settings.openai_model,
        # )
        pass

    async def chat(self, query: str, session_id: str | None = None) -> dict:
        """
        Process a user query using the RAG agent.

        Args:
            query: User's question or request
            session_id: Optional session ID for conversation continuity

        Returns:
            Dictionary containing:
            - answer: The agent's response
            - sources: List of sources used (if available)
            - session_id: Session ID for this conversation

        TODO: Implement this method
        Hint:
        1. Create or retrieve a conversation thread
        2. Add the user's message to the thread
        3. Run the agent to generate a response
        4. Extract and format the response
        5. Optionally extract sources from tool calls
        """
        # TODO: Implement chat logic
        # 1. Handle session management (create/get thread)
        # 2. Send message to agent
        # 3. Process response
        # 4. Extract sources if available
        raise NotImplementedError("Students need to implement chat method")

    def _extract_sources(self, response) -> list[dict] | None:
        """
        Extract sources from agent tool calls.

        Args:
            response: Agent response object

        Returns:
            List of source dictionaries or None

        This is a helper method to parse tool call results
        and extract source information for transparency.
        """
        # TODO: Optional - Implement source extraction
        # This helps provide transparency about where information comes from
        return None


# Convenience function for creating RAG agent instance
def create_rag_agent() -> RAGAgent:
    """
    Factory function to create a RAG agent instance.

    Returns:
        Configured RAGAgent instance
    """
    return RAGAgent()
