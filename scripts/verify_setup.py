#!/usr/bin/env python3
"""
Setup verification script for Week 1.

This script checks that:
1. All required files are present
2. Environment variables are set
3. Dependencies are installed
4. Qdrant collection is populated
5. Basic imports work

Run: python scripts/verify_setup.py
"""

import os
import sys
from pathlib import Path


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def check_files():
    """Check that all required files exist."""
    print_header("📁 Checking Project Files")

    required_files = [
        ".env.example",
        "README.md",
        "QUICKSTART.md",
        "ASSIGNMENT_CHECKLIST.md",
        "Dockerfile",
        "docker-compose.yml",
        "backend/pyproject.toml",
        "backend/src/main.py",
        "backend/src/config.py",
        "backend/src/agents/rag_agent.py",
        "backend/src/tools/vector_search.py",
        "backend/src/schemas/requests.py",
        "examples/01_openai_agents_basics.py",
        "examples/02_qdrant_ingestion.py",
        "examples/03_qdrant_search.py",
        "data/sample_docs/openai_agents_guide.md",
        "scripts/setup_qdrant.py",
    ]

    project_root = Path(__file__).parent.parent
    missing_files = []

    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)

    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files!")
        return False

    print(f"\n✅ All {len(required_files)} required files present!")
    return True


def check_env_vars():
    """Check that required environment variables are set."""
    print_header("🔑 Checking Environment Variables")

    required_vars = [
        "OPENAI_API_KEY",
        "QDRANT_URL",
        "QDRANT_API_KEY",
    ]

    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Show partial value for security
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var} = {masked}")
        else:
            print(f"❌ {var} is not set")
            missing_vars.append(var)

    if missing_vars:
        print(f"\n⚠️  Missing {len(missing_vars)} environment variables!")
        print("\nTo fix:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your API keys")
        print("3. Run this script again")
        return False

    print(f"\n✅ All {len(required_vars)} environment variables set!")
    return True


def check_dependencies():
    """Check that dependencies are installed."""
    print_header("📦 Checking Dependencies")

    required_packages = [
        ("fastapi", "FastAPI"),
        ("openai", "OpenAI"),
        ("qdrant_client", "Qdrant Client"),
        ("pydantic", "Pydantic"),
        ("pydantic_settings", "Pydantic Settings"),
        ("uvicorn", "Uvicorn"),
    ]

    missing_packages = []

    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name}")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n⚠️  Missing {len(missing_packages)} packages!")
        print("\nTo fix:")
        print("  cd backend")
        print("  uv sync")
        return False

    print(f"\n✅ All {len(required_packages)} dependencies installed!")
    return True


def check_qdrant():
    """Check Qdrant connection and collection."""
    print_header("🗄️  Checking Qdrant")

    try:
        from qdrant_client import QdrantClient

        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "course_documents")

        if not url or not api_key:
            print("⚠️  Qdrant credentials not set, skipping connection test")
            return True

        print("Connecting to Qdrant...")
        client = QdrantClient(url=url, api_key=api_key)

        print("✅ Connected to Qdrant")

        # Check collection
        try:
            collection = client.get_collection(collection_name)
            print(f"✅ Collection '{collection_name}' exists")
            print(f"   Points: {collection.points_count}")

            if collection.points_count == 0:
                print("\n⚠️  Collection is empty!")
                print("\nTo fix:")
                print("  cd backend")
                print("  uv run python ../scripts/setup_qdrant.py")
                return False

            return True

        except Exception as e:
            print(f"❌ Collection '{collection_name}' not found")
            print("\nTo fix:")
            print("  cd backend")
            print("  uv run python ../scripts/setup_qdrant.py")
            return False

    except Exception as e:
        print(f"❌ Error connecting to Qdrant: {e}")
        return False


def check_imports():
    """Check that project imports work."""
    print_header("🔬 Checking Project Imports")

    project_root = Path(__file__).parent.parent
    backend_src = project_root / "backend" / "src"

    # Add to Python path
    sys.path.insert(0, str(backend_src))

    try:
        print("Importing config...")
        from config import settings

        print("✅ config.settings")

        print("Importing schemas...")
        from schemas.requests import ChatRequest, ChatResponse

        print("✅ schemas.requests")

        print("Importing tools...")
        from tools.vector_search import VectorSearchTool

        print("✅ tools.vector_search")

        print("Importing agents...")
        from agents.rag_agent import RAGAgent

        print("✅ agents.rag_agent")

        print("Importing main app...")
        from main import app

        print("✅ main.app")

        print("\n✅ All imports successful!")
        return True

    except Exception as e:
        print(f"\n❌ Import error: {e}")
        print("\nThis might be expected if you haven't completed the assignment yet.")
        return False


def main():
    """Run all checks."""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   Week 1 Setup Verification Script                      ║
║   From Vibe to Live: Production AI Agents Course        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    results = {
        "Files": check_files(),
        "Environment Variables": check_env_vars(),
        "Dependencies": check_dependencies(),
        "Qdrant": check_qdrant(),
        "Imports": check_imports(),
    }

    print_header("📊 Verification Summary")

    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {check}")

    all_passed = all(results.values())

    if all_passed:
        print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ✅ All checks passed! You're ready to start Week 1!   ║
║                                                          ║
║   Next steps:                                            ║
║   1. Read QUICKSTART.md                                  ║
║   2. Review examples in examples/                        ║
║   3. Start implementing TODOs in backend/src/            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """)
        return 0
    else:
        print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ⚠️  Some checks failed. Fix the issues above.         ║
║                                                          ║
║   Need help? Check:                                      ║
║   - QUICKSTART.md for setup instructions                 ║
║   - backend/README.md for troubleshooting                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """)
        return 1


if __name__ == "__main__":
    sys.exit(main())
