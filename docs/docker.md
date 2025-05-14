# Docker Deployment Guide

This guide explains how to deploy NEURA using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10.0+
- Docker Compose 2.0.0+
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/neura.git
cd neura
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the service:
```bash
# Development environment
docker-compose up neura-dev

# Production environment
docker-compose up neura
```

## Docker Images

### Production Image

The production image (`Dockerfile`) is optimized for size and security:

- Multi-stage build to minimize image size
- Only production dependencies included
- Runs as non-root user
- Minimal system packages

### Development Image

The development image (`Dockerfile.dev`) includes additional tools:

- Development dependencies
- Hot-reloading support
- Debugging tools
- Source code mounted as volume

## Docker Compose

The `docker-compose.yml` file defines two services:

### Production Service

```yaml
neura:
  build:
    context: .
    dockerfile: Dockerfile
  volumes:
    - ./data:/app/data
    - ./.env:/app/.env
  environment:
    - PYTHONPATH=/app
    - PYTHONUNBUFFERED=1
```

### Development Service

```yaml
neura-dev:
  build:
    context: .
    dockerfile: Dockerfile.dev
  volumes:
    - .:/app
    - ./data:/app/data
    - ./.env:/app/.env
  environment:
    - PYTHONPATH=/app
    - PYTHONUNBUFFERED=1
    - ENVIRONMENT=development
```

## Volume Mounts

- `./data:/app/data`: Persistent storage for memory and other data
- `./.env:/app/.env`: Environment configuration
- `.:/app`: Source code (development only)

## Environment Variables

Required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `PYTHONPATH`: Set to `/app` for proper module resolution
- `PYTHONUNBUFFERED`: Set to `1` for immediate output
- `ENVIRONMENT`: Set to `development` for development mode

## Running Commands

### Using Docker Compose

```bash
# Run a specific command
docker-compose run neura run "Research quantum computing"

# Run with custom parameters
docker-compose run neura run "Research AI" --model gpt-4 --temperature 0.8

# Access memory
docker-compose run neura memory --query "quantum computing"
```

### Using Docker Directly

```bash
# Build the image
docker build -t neura .

# Run a command
docker run -v $(pwd)/data:/app/data -v $(pwd)/.env:/app/.env neura run "Research quantum computing"
```

## Best Practices

1. **Data Persistence**
   - Always mount the `data` directory for persistence
   - Use named volumes in production

2. **Security**
   - Never commit `.env` files
   - Use secrets management in production
   - Run as non-root user

3. **Performance**
   - Use production image in production
   - Enable caching for faster builds
   - Use multi-stage builds

4. **Development**
   - Use development image for local development
   - Mount source code as volume
   - Enable hot-reloading

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Fix data directory permissions
   sudo chown -R 1000:1000 data/
   ```

2. **Module Not Found**
   ```bash
   # Ensure PYTHONPATH is set
   export PYTHONPATH=/app
   ```

3. **Playwright Issues**
   ```bash
   # Reinstall Playwright browsers
   docker-compose run neura-dev playwright install
   ```

### Getting Help

- Check the [GitHub Issues](https://github.com/yourusername/neura/issues)
- Join our [Discord Community](https://discord.gg/neura)
- Read the [Documentation](https://neura.readthedocs.io) 