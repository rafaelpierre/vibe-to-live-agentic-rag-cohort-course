# Federal Reserve Data Pipeline

This folder contains scripts for fetching and processing Federal Reserve speeches and testimony data.

## Setup

```bash
cd scripts/data_pipeline
uv sync
```

## Scripts

### `fetch_fed_speeches.py`

Crawls the Federal Reserve RSS feed, scrapes speech content, and saves to JSONL format.

**Usage:**
```bash
uv run python fetch_fed_speeches.py
```

**Output:**
- `../../data/fed_speeches/speeches.jsonl` - All speeches in JSONL format
- `../../data/fed_speeches/metadata.json` - Summary metadata

**Options:**
- `--limit N` - Limit to N speeches (default: all)
- `--output PATH` - Custom output path

**Example:**
```bash
# Fetch all speeches (default)
uv run python fetch_fed_speeches.py

# Fetch only 5 speeches for testing
uv run python fetch_fed_speeches.py --limit 5
```

### `ingest_fed_speeches.py`

Ingests Federal Reserve speeches into Qdrant using FastEmbed for vector embeddings.

**Prerequisites:**
Set environment variables:
```bash
export QDRANT_API_KEY="your-qdrant-api-key"
export QDRANT_URL="https://your-cluster.qdrant.io"  # Optional
```

**Usage:**
```bash
uv run python ingest_fed_speeches.py
```

**What it does:**
1. **Loads Fed speeches** from `../../data/fed_speeches/speeches.jsonl`
2. **Connects to Qdrant Cloud** using your API key
3. **Creates a collection** named `fed_speeches` with COSINE distance
4. **Embeds documents** using the `BAAI/bge-small-en` model via FastEmbed
5. **Uploads vectors and metadata** to Qdrant
6. **Verifies ingestion** with a sample search

**Collection Schema:**
- **Collection name:** `fed_speeches`
- **Embedding model:** `BAAI/bge-small-en`
- **Vector size:** Automatically determined by the model
- **Distance metric:** COSINE

**Metadata Structure:**
Each document includes:
- `title`: Speech title
- `url`: Original URL
- `author`: Speaker name  
- `subject`: Speech subject
- `description`: Brief description
- `category`: Document category (usually "Speech")
- `pub_date`: Publication date
- `content_length`: Character count
- `scraped_at`: Timestamp when scraped
- `document`: Full speech content text
1. Reads speeches from `data/fed_speeches/speeches.jsonl`
2. Chunks long speeches into manageable pieces (1000 chars with 200 char overlap)
3. Generates embeddings using OpenAI
4. Creates Qdrant collection `fed_speeches`
5. Uploads all chunks with metadata

**Prerequisites:**
- Run `fetch_fed_speeches.py` first to download speeches
- Set environment variables in `.env` file

### `setup_qdrant.py`

Populates Qdrant with sample course documents (alternative to Fed speeches).

**Usage:**
```bash
cd ../../backend
uv run python ../scripts/data_pipeline/setup_qdrant.py
```

### `verify_setup.py`

Verifies that the Week 1 project is set up correctly.

**Usage:**
```bash
cd ../..
uv run python scripts/data_pipeline/verify_setup.py
```

## Data Format

Each speech is saved as a JSON line with the following structure:

```json
{
  "title": "Powell, Economic Outlook",
  "url": "https://www.federalreserve.gov/newsevents/speech/powell20250923a.htm",
  "category": "Speech",
  "pub_date": "2025-09-23T16:35:00+00:00",
  "description": "Speech At the Greater Providence Chamber...",
  "content": "Full speech text...",
  "author": "Powell",
  "subject": "Economic Outlook",
  "scraped_at": "2025-10-03T10:00:00+00:00"
}
```
