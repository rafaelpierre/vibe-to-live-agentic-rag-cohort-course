"""
Example 01: OpenAI Agents SDK Basics

This example introduces the OpenAI Agents SDK and shows:
1. How to create a simple agent
2. How to define custom tools/functions
3. How to run an agent and get responses

Run this example:
    python examples/01_openai_agents_basics.py
"""

import os

from openai import OpenAI
from openai.agents import Agent


# Define a custom tool function
def get_weather(location: str) -> str:
    """
    Get the weather for a specific location.

    This is a mock function - in production, you'd call a real weather API.

    Args:
        location: City name or location

    Returns:
        Weather information as a string
    """
    # Mock weather data
    mock_weather = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Cloudy, 65°F",
        "London": "Rainy, 58°F",
        "Tokyo": "Clear, 68°F",
    }

    weather = mock_weather.get(location, "Unknown location")
    return f"Weather in {location}: {weather}"


def main():
    """Run the basic agent example."""
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Create an agent with a tool
    agent = Agent(
        name="Weather Assistant",
        instructions="""
        You are a helpful weather assistant.
        When users ask about weather, use the get_weather tool to provide accurate information.
        Be friendly and conversational.
        """,
        tools=[get_weather],
        model="gpt-4o-mini",
    )

    print("🤖 OpenAI Agents SDK - Basic Example")
    print("=" * 50)

    # Example 1: Simple interaction without tools
    print("\n📝 Example 1: Simple greeting")
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content="Hello! Who are you?"
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=agent.id,
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        print(f"Agent: {response}")

    # Example 2: Using the tool
    print("\n📝 Example 2: Using the weather tool")
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="What's the weather like in San Francisco?",
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=agent.id,
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        print(f"Agent: {response}")

    print("\n✅ Example complete!")
    print("\n💡 Key Takeaways:")
    print("   - Agents can use custom tools/functions")
    print("   - Tools are automatically called when needed")
    print("   - Conversations are managed through threads")
    print("   - The SDK handles the function calling automatically")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set it in your .env file or export it:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        exit(1)

    main()
