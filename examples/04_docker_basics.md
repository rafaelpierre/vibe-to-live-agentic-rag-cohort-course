# Docker Basics Cheatsheet

## What is Docker?

Docker is a platform for developing, shipping, and running applications in containers. Containers package an application with all its dependencies, ensuring it runs consistently across different environments.

## Key Concepts

### 1. **Container**
- Lightweight, standalone executable package
- Includes code, runtime, libraries, and settings
- Isolated from other containers and the host system

### 2. **Image**
- Template for creating containers
- Built from a Dockerfile
- Can be shared via Docker Hub or private registries

### 3. **Dockerfile**
- Text file with instructions to build an image
- Defines base image, dependencies, and application setup

### 4. **Docker Compose**
- Tool for defining multi-container applications
- Uses YAML configuration file
- Manages container networking, volumes, and dependencies

## Essential Docker Commands

### Image Management
```bash
# Build an image
docker build -t my-app:latest .

# List images
docker images

# Remove an image
docker rmi my-app:latest

# Pull an image from registry
docker pull python:3.11-slim
```

### Container Management
```bash
# Run a container
docker run -d --name my-container -p 8000:8000 my-app:latest

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop my-container

# Start a stopped container
docker start my-container

# Remove a container
docker rm my-container

# View container logs
docker logs my-container

# Follow logs in real-time
docker logs -f my-container

# Execute command in running container
docker exec -it my-container /bin/bash
```

### Docker Compose Commands
```bash
# Start services
docker-compose up

# Start services in detached mode
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Rebuild images
docker-compose build

# Restart services
docker-compose restart
```

## Dockerfile Best Practices

### 1. Use Official Base Images
```dockerfile
FROM python:3.11-slim
```

### 2. Minimize Layers
```dockerfile
# Bad: Multiple RUN commands
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Good: Combine into one
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Use .dockerignore
Create a `.dockerignore` file to exclude unnecessary files:
```
.git
.env
__pycache__
*.pyc
.venv
node_modules
```

### 4. Run as Non-Root User
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 5. Use Multi-Stage Builds
```dockerfile
# Build stage
FROM python:3.11 as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]
```

## Docker Compose Example

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=true
    env_file:
      - .env
    volumes:
      - ./src:/app/src
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Common Use Cases for This Course

### 1. Building the API Image
```bash
cd /workspaces/vibe-to-live-agentic-rag-cohort-course
docker build -t agentic-rag-api:latest .
```

### 2. Running with Docker Compose
```bash
# Start the API
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop everything
docker-compose down
```

### 3. Testing Changes
```bash
# Rebuild after code changes
docker-compose build api

# Restart the service
docker-compose restart api
```

### 4. Debugging
```bash
# Enter the running container
docker exec -it agentic-rag-api /bin/bash

# Check environment variables
docker exec agentic-rag-api env

# View container resource usage
docker stats
```

## Health Checks

Health checks ensure your container is running correctly:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

Check health status:
```bash
docker inspect --format='{{.State.Health.Status}}' my-container
```

## Networking

### Port Mapping
```bash
# Map container port 8000 to host port 3000
docker run -p 3000:8000 my-app
```

### Container-to-Container Communication
Containers in the same Docker Compose network can communicate using service names:
```python
# Connect to database using service name
DATABASE_URL = "postgresql://user:pass@db:5432/mydb"
```

## Volume Management

### Named Volumes
```bash
# Create volume
docker volume create my-data

# List volumes
docker volume ls

# Remove volume
docker volume rm my-data
```

### Bind Mounts (for development)
```bash
# Mount local directory to container
docker run -v $(pwd)/src:/app/src my-app
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs my-container

# Check exit code
docker inspect my-container --format='{{.State.ExitCode}}'
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Or use different port
docker run -p 8001:8000 my-app
```

### Out of Disk Space
```bash
# Remove unused containers, images, and volumes
docker system prune -a

# Remove only volumes
docker volume prune
```

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Hub](https://hub.docker.com/)

## Week 1 Assignment Tips

For your assignment, you'll need to:

1. ✅ Understand how the Dockerfile builds your application
2. ✅ Use docker-compose to run the API locally
3. ✅ View logs to debug your RAG implementation
4. ✅ Test your `/chat` endpoint against the containerized API

Remember: Docker ensures your application runs the same way everywhere - on your machine, in CI/CD, and in production!
