# Multi-stage build for Python backend using uv
# Stage 1: Build stage with uv for dependency resolution and installation
FROM python:3.13-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set environment variables for uv
ENV UV_SYSTEM_PYTHON=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Set FastEmbed cache directory to avoid permission issues
ENV FASTEMBED_CACHE_PATH=/tmp/fastembed_cache

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv sync (much faster than pip install)
RUN uv sync --frozen --no-dev

# The virtual environment is created automatically by uv sync at .venv
ENV PATH="/app/.venv/bin:$PATH"

# Preload FastEmbed model to avoid permission issues at runtime
RUN mkdir -p /tmp/fastembed_cache && \
    FASTEMBED_CACHE_PATH=/tmp/fastembed_cache python -c "from fastembed import TextEmbedding; model = TextEmbedding('BAAI/bge-small-en'); print('Model loaded successfully')" && \
    ls -la /tmp/fastembed_cache

# Stage 2: Runtime stage with minimal dependencies
FROM python:3.13-slim as runtime

# Install only necessary system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Set FastEmbed cache directory before copying cache
ENV FASTEMBED_CACHE_PATH=/tmp/fastembed_cache

# Copy FastEmbed cache from builder stage
COPY --from=builder --chown=root:root /tmp/fastembed_cache /tmp/fastembed_cache

# Make sure to use venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/src

# Set FastEmbed cache directory
ENV FASTEMBED_CACHE_PATH=/tmp/fastembed_cache

# Set working directory
WORKDIR /app

# Copy application source code
COPY src/ ./src/

# Verify cache exists and change ownership to non-root user
RUN ls -la /tmp/fastembed_cache && \
    chown -R appuser:appuser /app /tmp/fastembed_cache

USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "src.web.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]