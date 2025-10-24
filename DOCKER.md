# Agentic RAG Application - Docker Deployment

## Quick Start

### Build and run all services:

```bash
docker compose up --build
```

### Services:
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Backend Health**: http://localhost:8000/health
- **Frontend Health**: http://localhost:3000/health

## Environment Variables

All environment variables should be set in your host environment before running docker compose.

### Required Backend Variables:

```bash
export OPENAI_API_KEY="your-openai-key"
export OPENAI_API_ENDPOINT="https://api.openai.com/v1"
export QDRANT_URL="your-qdrant-url"
export QDRANT_API_KEY="your-qdrant-key"
export PHOENIX_API_KEY="your-phoenix-key"
export PHOENIX_COLLECTOR_ENDPOINT="your-phoenix-endpoint"
```

### Optional Frontend Variables:

```bash
# Override the backend API URL (defaults to http://localhost:8000)
export VITE_API_URL="https://your-backend-url.com"
```

## Build with Custom API URL

To build the frontend with a specific backend URL:

```bash
VITE_API_URL=https://api.example.com docker compose up --build
```

## Production Deployment

### Backend Only:
```bash
docker compose up -d backend-api
```

### Frontend Only:
```bash
docker compose up -d frontend
```

### Stop All Services:
```bash
docker compose down
```

### View Logs:
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend-api
docker compose logs -f frontend
```

## Architecture

```
┌─────────────┐         ┌──────────────┐
│   Frontend  │────────▶│  Backend API │
│  (Nginx)    │         │  (FastAPI)   │
│  Port 3000  │         │  Port 8000   │
└─────────────┘         └──────────────┘
                              │
                              ├─────▶ OpenAI
                              ├─────▶ Qdrant
                              └─────▶ Phoenix
```

## Development

For local development without Docker, see:
- `backend/README.md`
- `frontend/README.md`
