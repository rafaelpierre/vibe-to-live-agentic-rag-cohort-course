#!/usr/bin/env python3
"""
Solution Checker for Vector Search TODO Assignment

This script helps students verify their implementation step by step.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_imports():
    """Check if the file can be imported."""
    print("🔍 Step 1: Checking imports...")
    try:
        from tools.vector_search_todo import VectorSearchTool, search_knowledge_base
        print("✅ Imports successful!")
        return True, VectorSearchTool, search_knowledge_base
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("   Fix syntax errors before proceeding.")
        return False, None, None


def check_initialization(VectorSearchTool):
    """Check if the tool can be initialized."""
    print("\n🔍 Step 2: Checking initialization...")
    
    # Set test env vars
    os.environ["QDRANT_URL"] = "https://test.example.com"
    os.environ["QDRANT_API_KEY"] = "test-key"
    
    try:
        tool = VectorSearchTool()
        
        # Check attributes
        checks = {
            "qdrant_url is set": tool.qdrant_url is not None,
            "qdrant_api_key is set": tool.qdrant_api_key is not None,
            "qdrant_client is initialized": tool.qdrant_client is not None,
            "collection_name is set": tool.collection_name is not None,
            "model_name is set": tool.model_name is not None,
        }
        
        all_passed = all(checks.values())
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        if all_passed:
            print("✅ Initialization complete!")
        else:
            print("❌ Some initialization checks failed.")
            print("   Review TODOs 1-4.")
        
        return all_passed
        
    except ValueError as e:
        if "must be provided" in str(e):
            print("✅ Validation error raised correctly!")
            print("   (This is expected when credentials are missing)")
            return True
        else:
            print(f"❌ Unexpected ValueError: {e}")
            return False
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print("   Check TODOs 1-4.")
        return False


def check_search_method(VectorSearchTool):
    """Check if search method is implemented."""
    print("\n🔍 Step 3: Checking search method...")
    
    os.environ["QDRANT_URL"] = "https://test.example.com"
    os.environ["QDRANT_API_KEY"] = "test-key"
    
    try:
        tool = VectorSearchTool()
        
        # Check if method exists and has correct signature
        import inspect
        sig = inspect.signature(tool.search)
        params = list(sig.parameters.keys())
        
        checks = {
            "search method exists": hasattr(tool, 'search'),
            "has 'query' parameter": 'query' in params,
            "has 'limit' parameter": 'limit' in params,
        }
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        if all(checks.values()):
            print("✅ Search method signature correct!")
            print("   Note: Full testing requires mocking or live Qdrant connection")
            return True
        else:
            print("❌ Search method has issues.")
            print("   Review TODOs 5-6.")
            return False
            
    except Exception as e:
        print(f"❌ Error checking search method: {e}")
        return False


def check_verify_collection(VectorSearchTool):
    """Check if verify_collection is implemented."""
    print("\n🔍 Step 4: Checking verify_collection method...")
    
    os.environ["QDRANT_URL"] = "https://test.example.com"
    os.environ["QDRANT_API_KEY"] = "test-key"
    
    try:
        tool = VectorSearchTool()
        
        checks = {
            "verify_collection method exists": hasattr(tool, 'verify_collection'),
            "method is callable": callable(getattr(tool, 'verify_collection', None)),
        }
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        if all(checks.values()):
            print("✅ verify_collection method exists!")
            print("   Note: Full testing requires live Qdrant connection")
            return True
        else:
            print("❌ verify_collection has issues.")
            print("   Review TODO 7.")
            return False
            
    except Exception as e:
        print(f"❌ Error checking verify_collection: {e}")
        return False


def check_tool_function(search_knowledge_base):
    """Check if the tool function is implemented."""
    print("\n🔍 Step 5: Checking search_knowledge_base function...")
    
    checks = {
        "function exists": search_knowledge_base is not None,
        "function is callable": callable(search_knowledge_base),
    }
    
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {check}")
    
    if all(checks.values()):
        print("✅ search_knowledge_base function exists!")
        print("   Note: Full testing requires live Qdrant connection")
        return True
    else:
        print("❌ search_knowledge_base has issues.")
        print("   Review TODO 8.")
        return False


def run_full_tests():
    """Run the full test suite."""
    print("\n🧪 Running full test suite...")
    print("=" * 60)
    
    import subprocess
    result = subprocess.run(
        ["uv", "run", "pytest", "tests/test_vector_search.py", "-v"],
        cwd=os.path.dirname(__file__),
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ All tests passed!")
        print("\n🎉 Congratulations! Your implementation is complete!")
        return True
    else:
        print("❌ Some tests failed.")
        print("\nTest output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        return False


def main():
    """Main checker function."""
    print("=" * 60)
    print("🎓 Vector Search TODO Assignment - Solution Checker")
    print("=" * 60)
    
    # Step 1: Check imports
    success, VectorSearchTool, search_knowledge_base = check_imports()
    if not success:
        print("\n❌ Fix import errors before continuing.")
        return
    
    # Step 2: Check initialization
    success = check_initialization(VectorSearchTool)
    if not success:
        print("\n⚠️  Initialization issues found. Continue checking other parts...")
    
    # Step 3: Check search method
    check_search_method(VectorSearchTool)
    
    # Step 4: Check verify_collection
    check_verify_collection(VectorSearchTool)
    
    # Step 5: Check tool function
    check_tool_function(search_knowledge_base)
    
    # Final step: Run full tests
    print("\n" + "=" * 60)
    response = input("Run full test suite? (y/n): ").lower()
    if response == 'y':
        run_full_tests()
    else:
        print("\nTo run tests manually:")
        print("  cd backend")
        print("  uv run pytest tests/test_vector_search.py -v")
    
    print("\n" + "=" * 60)
    print("📚 Resources:")
    print("  - Guide: src/tools/VECTOR_SEARCH_GUIDE.md")
    print("  - Reference: src/tools/vector_search.py")
    print("  - Tests: tests/test_vector_search.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
