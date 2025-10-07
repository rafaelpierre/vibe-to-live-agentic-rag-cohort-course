# Ingestion Pipeline Fixes

## Issues Identified and Resolved

### Issue 1: Speaker Field Not Being Captured ✅ FIXED

**Problem:**
- The JSONL data uses the field name `"author"` but the ingestion script was reading `"speaker"`
- This resulted in empty speaker fields in the Qdrant collection

**Example from data:**
```json
{
  "title": "Jefferson, Monetary Policy Frameworks and the U.S. Economic Outlook",
  "author": "Jefferson",  // ← Field name is "author"
  "subject": "Monetary Policy Frameworks and the U.S. Economic Outlook"
}
```

**Fix Applied:**
Changed line in `ingest_fed_speeches.py`:
```python
# Before:
"speaker": speech.get("speaker", ""),

# After:
"speaker": speech.get("author", ""),  # Fixed: field is "author" in JSONL
```

---

### Issue 2: Documents Too Long for Embedding Model ✅ FIXED

**Problem:**
- The BAAI/bge-small-en model has a **512 token limit** (~2000 characters max)
- Speeches are very long (example: 16,529 characters)
- Without chunking, most content beyond 2000 chars gets truncated and lost
- This severely impacts search quality and retrieval accuracy

**Why Vector Size 384 is NOT the Issue:**
- 384 is the **output embedding dimension** (vector size)
- The input token limit (512 tokens) is the actual constraint
- These are two different concepts:
  - **Input limit:** 512 tokens (~2000 characters) - how much text the model can process
  - **Output dimension:** 384 numbers - the size of the resulting embedding vector

**Solution Implemented:**
Added intelligent text chunking with overlap:

1. **Added chunking function** (`chunk_text()`):
   - Splits speeches into 1500-character chunks
   - 200-character overlap between chunks for context continuity
   - Smart boundary detection (sentences, paragraphs, words)

2. **Updated ingestion logic**:
   - Each speech is now split into multiple chunks
   - Each chunk gets its own embedding
   - Metadata tracks chunk position and relationships

3. **New metadata fields**:
   ```python
   {
       "chunk_index": 0,        # Which chunk this is (0-based)
       "total_chunks": 12,      # Total chunks from this speech
       "speech_id": 5,          # ID of original speech
       "document": "<chunk>"    # The actual chunk text
   }
   ```

**Benefits:**
- ✅ All content is now searchable (nothing gets truncated)
- ✅ Better semantic relevance (focused chunks vs. entire document)
- ✅ More precise search results (can pinpoint specific sections)
- ✅ Maintains context with overlapping chunks

**Example:**
A 16,529 character speech now becomes ~12 chunks of ~1,500 characters each, all fully searchable.

---

## Impact on Collection

**Before:**
- 15 speeches → 15 vectors in Qdrant
- Most content beyond 2000 chars lost
- Speaker field empty

**After:**
- 15 speeches → ~150-200 vectors in Qdrant (varies by speech length)
- All content fully embedded and searchable
- Speaker field populated correctly

---

## Testing the Fixes

### Re-run the ingestion script:

```bash
cd scripts/data_pipeline
uv run python ingest_fed_speeches.py
```

### Expected Output:
```
3️⃣  Preparing documents for embedding...
   Speech 1: 'Jefferson, Monetary Policy Frameworks...' -> 12 chunks
   Speech 2: 'Waller, The Next Frontier of Payments...' -> 11 chunks
   ...
✅ Prepared 180 document chunks from 15 speeches

6️⃣  Verifying ingestion with test search...
✅ Collection now contains 180 chunks (from 15 speeches)

📊 Top result:
   Score: 0.8542
   Title: Jefferson, Monetary Policy Frameworks and the U.S. Economic Outlook
   Speaker: Jefferson  ← Now populated!
   Chunk: 3/12        ← Shows chunk position
```

### Verify in Qdrant:
You should now see:
- ✅ `speaker` field populated with author names
- ✅ Multiple chunks per speech
- ✅ Better search quality with more relevant results

---

## Additional Notes

### Chunk Size Considerations
- **1500 characters** balances detail vs. context
- Smaller chunks (500-1000): More precise but less context
- Larger chunks (2000-3000): Would exceed model limits
- 200-char overlap ensures context continuity across boundaries

### Model Limits Reference
- **BAAI/bge-small-en:**
  - Input: 512 tokens (~2000 characters)
  - Output: 384-dimensional vector
  - Language: English
  - Use case: Fast, efficient embedding for search

### Performance
- Chunking adds minimal processing time
- Smart boundary detection preserves sentence integrity
- Overlap prevents information loss at chunk boundaries
