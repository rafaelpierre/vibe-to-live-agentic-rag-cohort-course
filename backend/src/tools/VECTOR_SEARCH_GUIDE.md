# Vector Search Tool - Student Guide

## Overview
Complete the implementation of `vector_search_todo.py` by following the TODO items. This file will help you understand how to build a vector search tool using Qdrant and FastEmbed.

## Prerequisites
- Qdrant collection `fed_speeches` must exist (run `scripts/data_pipeline/ingest_fed_speeches.py`)
- Environment variables `QDRANT_URL` and `QDRANT_API_KEY` must be set

## TODO Checklist

### ✅ TODO 1: Get Environment Variables
**Location:** `__init__` method  
**Task:** Read QDRANT_URL and QDRANT_API_KEY from environment variables

**Hints:**
- Use `os.getenv("VARIABLE_NAME")` to read environment variables
- Use the `or` operator to use parameters if provided, otherwise fall back to env vars
- Pattern: `self.variable = parameter or os.getenv("ENV_VAR")`

**Example:**
```python
self.qdrant_url = qdrant_url or os.getenv("QDRANT_URL")
```

---

### ✅ TODO 2: Validate Credentials
**Location:** `__init__` method  
**Task:** Ensure both URL and API key are provided

**Hints:**
- Check if either value is `None` or empty
- Raise `ValueError` with a helpful message if validation fails
- Use an `if` statement: `if not self.qdrant_url or not self.qdrant_api_key:`

**Example:**
```python
if not self.qdrant_url or not self.qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY must be provided or set as environment variables")
```

---

### ✅ TODO 3: Initialize Qdrant Client
**Location:** `__init__` method  
**Task:** Create a QdrantClient instance

**Hints:**
- Import is already done: `from qdrant_client import QdrantClient`
- Pass `url` and `api_key` as parameters
- Store the client in `self.qdrant_client`

**Example:**
```python
self.qdrant_client = QdrantClient(
    url=self.qdrant_url,
    api_key=self.qdrant_api_key,
)
```

---

### ✅ TODO 4: Set Collection Name
**Location:** `__init__` method  
**Task:** Set the collection name with a default value

**Hints:**
- Use the same pattern as TODO 1
- Default collection name is `"fed_speeches"`
- Pattern: `self.collection_name = collection_name or "default_value"`

**Example:**
```python
self.collection_name = collection_name or "fed_speeches"
```

---

### ✅ TODO 5: Perform Vector Search
**Location:** `search` method  
**Task:** Call Qdrant's query_points method to search for documents

**Hints:**
- Use `self.qdrant_client.query_points()`
- Pass three parameters: `collection_name`, `query`, `limit`
- The `query` parameter should be: `models.Document(text=query, model=self.model_name)`
- Access the results with `.points` attribute

**Example:**
```python
search_results = self.qdrant_client.query_points(
    collection_name=self.collection_name,
    query=models.Document(text=query, model=self.model_name),
    limit=limit
).points
```

**Why this works:**
- FastEmbed automatically generates embeddings when you use `models.Document`
- No need to manually call an embedding API!

---

### ✅ TODO 6: Format Search Results
**Location:** `search` method  
**Task:** Loop through results and format them into a list of dictionaries

**Hints:**
- Use a `for` loop to iterate through `search_results`
- Each result has:
  - `.score` (float) - similarity score
  - `.payload` (dict) - document metadata and content
- Use `.get("key", "")` to safely access dictionary values with defaults
- Create a dict with three keys: `"content"`, `"metadata"`, `"score"`

**Structure to return:**
```python
{
    "content": "...",
    "metadata": {
        "title": "...",
        "speaker": "...",
        "pub_date": "...",
        "category": "...",
        "url": "...",
        "description": "..."
    },
    "score": 0.95
}
```

**Example:**
```python
formatted_results = []
for result in search_results:
    formatted_results.append({
        "content": result.payload.get("document", ""),
        "metadata": {
            "title": result.payload.get("title", ""),
            "speaker": result.payload.get("speaker", ""),
            "pub_date": result.payload.get("pub_date", ""),
            "category": result.payload.get("category", ""),
            "url": result.payload.get("url", ""),
            "description": result.payload.get("description", ""),
        },
        "score": result.score
    })
```

---

### ✅ TODO 7: Verify Collection Exists
**Location:** `verify_collection` method  
**Task:** Check if the collection exists and return its information

**Hints:**
- Use a try/except block
- In the `try` block:
  - Call `self.qdrant_client.get_collection(self.collection_name)`
  - Extract: `points_count`, `vector_size`, `distance`
  - Return a dict with `exists=True` and the info
- In the `except` block:
  - Return a dict with `exists=False` and the error message

**Example:**
```python
try:
    collection_info = self.qdrant_client.get_collection(self.collection_name)
    return {
        "exists": True,
        "points_count": collection_info.points_count,
        "vector_size": collection_info.config.params.vectors.size,
        "distance": collection_info.config.params.vectors.distance
    }
except Exception as e:
    return {
        "exists": False,
        "error": str(e)
    }
```

---

### ✅ TODO 8: Implement search_knowledge_base Function
**Location:** `search_knowledge_base` function  
**Task:** Create a wrapper function for OpenAI Agents SDK

**Hints:**
- This function should:
  1. Create a `VectorSearchTool` instance
  2. Call `.search()` method
  3. Format results as a readable string
  4. Handle the case when no results are found
- Use try/except to catch and report errors
- Format the output to be human-readable

**Example:**
```python
try:
    # Create tool instance
    tool = VectorSearchTool()
    
    # Perform search
    results = tool.search(query, limit=limit)
    
    # Handle empty results
    if not results:
        return f"No results found for query: '{query}'"
    
    # Format output
    formatted_output = f"Found {len(results)} relevant documents:\n\n"
    
    for idx, result in enumerate(results, 1):
        formatted_output += f"--- Result {idx} (Score: {result['score']:.4f}) ---\n"
        formatted_output += f"Title: {result['metadata']['title']}\n"
        formatted_output += f"Speaker: {result['metadata']['speaker']}\n"
        formatted_output += f"Date: {result['metadata']['pub_date']}\n"
        formatted_output += f"Category: {result['metadata']['category']}\n"
        
        # Truncate content to 300 chars
        content = result['content']
        snippet = content[:300] + "..." if len(content) > 300 else content
        formatted_output += f"Content: {snippet}\n\n"
    
    return formatted_output
    
except Exception as e:
    return f"Error searching knowledge base: {str(e)}"
```

---

## Testing Your Implementation

### Step 1: Run the Unit Tests
```bash
cd backend
uv run pytest tests/test_vector_search.py -v
```

All 20 tests should pass if your implementation is correct!

### Step 2: Manual Testing
Create a test script to try your implementation:

```python
from tools.vector_search_todo import VectorSearchTool, search_knowledge_base

# Test 1: Initialize tool
tool = VectorSearchTool()

# Test 2: Verify collection
info = tool.verify_collection()
print(f"Collection exists: {info['exists']}")
print(f"Points: {info.get('points_count', 'N/A')}")

# Test 3: Perform search
results = tool.search("monetary policy and interest rates", limit=3)
print(f"\nFound {len(results)} results")

for i, result in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(f"  Score: {result['score']:.4f}")
    print(f"  Title: {result['metadata']['title']}")

# Test 4: Use the tool function
output = search_knowledge_base("inflation and economic growth")
print("\n" + output)
```

---

## Common Mistakes to Avoid

1. **Forgetting to handle None values**
   - Always use `.get()` with defaults when accessing dictionary values
   - Check for None before using values

2. **Not using the .points attribute**
   - `query_points()` returns an object, access results with `.points`

3. **Wrong model in Document**
   - Always use `self.model_name` when creating `models.Document`

4. **Forgetting environment variables**
   - Make sure `.env` file has `QDRANT_URL` and `QDRANT_API_KEY`

5. **Not handling exceptions**
   - Always wrap external API calls in try/except blocks

---

## Need Help?

- Check the complete implementation in `vector_search.py`
- Run the tests to see what's failing
- Review the error messages carefully
- Look at `examples/03_qdrant_search.py` for usage examples

---

## Success Criteria

Your implementation is complete when:
- ✅ All 20 unit tests pass
- ✅ You can initialize VectorSearchTool without errors
- ✅ Search returns properly formatted results
- ✅ verify_collection works correctly
- ✅ search_knowledge_base returns readable output

Good luck! 🚀
