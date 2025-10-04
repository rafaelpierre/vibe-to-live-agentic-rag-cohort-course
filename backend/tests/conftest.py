"""
Pytest configuration for the test suite.
"""

import os
import sys
from pathlib import Path

import pytest

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def test_env():
    """Set up test environment variables."""
    # These should be set in your .env file
    # This fixture just ensures they're available during tests
    required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]

    for var in required_vars:
        if not os.getenv(var):
            pytest.skip(f"Missing required environment variable: {var}")


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables from .env file."""
    from dotenv import load_dotenv

    # Load from project root
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
