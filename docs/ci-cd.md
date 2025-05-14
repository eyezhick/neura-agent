# CI/CD Pipeline Guide

This guide explains NEURA's Continuous Integration and Continuous Deployment pipeline.

## Overview

The CI/CD pipeline is implemented using GitHub Actions and consists of two main workflows:

1. **CI Workflow** (`ci.yml`)
   - Runs on every push and pull request
   - Tests and lints the code
   - Builds and pushes Docker images

2. **Release Workflow** (`release.yml`)
   - Runs on version tag pushes
   - Publishes to PyPI
   - Creates GitHub releases

## CI Workflow

### Jobs

1. **Test Job**
   - Runs on Ubuntu latest
   - Python 3.9
   - Steps:
     - Set up Python
     - Install Poetry
     - Install dependencies
     - Install Playwright browsers
     - Run tests
     - Run linting

2. **Docker Job**
   - Runs after successful tests
   - Steps:
     - Set up Docker Buildx
     - Login to DockerHub
     - Build and push images

### Configuration

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9]
    # ... test job steps

  docker:
    runs-on: ubuntu-latest
    needs: test
    # ... docker job steps
```

## Release Workflow

### Jobs

1. **Release Job**
   - Runs on version tag pushes
   - Steps:
     - Set up Python
     - Install Poetry
     - Configure PyPI token
     - Build and publish package
     - Create GitHub release

### Configuration

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    # ... release job steps
```

## Required Secrets

The following secrets must be configured in your GitHub repository:

1. **DockerHub**
   - `DOCKERHUB_USERNAME`: Your DockerHub username
   - `DOCKERHUB_TOKEN`: Your DockerHub access token

2. **PyPI**
   - `PYPI_TOKEN`: Your PyPI API token

## Making a Release

1. Update version in `pyproject.toml`:
```toml
[tool.poetry]
version = "0.1.0"  # Update this
```

2. Create and push a version tag:
```bash
git tag v0.1.0
git push origin v0.1.0
```

3. The release workflow will:
   - Build the package
   - Publish to PyPI
   - Create a GitHub release
   - Push Docker images

## Best Practices

1. **Versioning**
   - Use semantic versioning
   - Update version in `pyproject.toml`
   - Create annotated tags

2. **Testing**
   - Write comprehensive tests
   - Maintain high test coverage
   - Test all Python versions

3. **Linting**
   - Follow style guides
   - Use automated tools
   - Fix issues promptly

4. **Documentation**
   - Update docs with changes
   - Include release notes
   - Document breaking changes

## Troubleshooting

### Common Issues

1. **Test Failures**
   - Check test logs
   - Verify dependencies
   - Update test cases

2. **Build Failures**
   - Check Docker logs
   - Verify Dockerfile
   - Check resource limits

3. **Deployment Failures**
   - Verify secrets
   - Check PyPI access
   - Verify package metadata

### Getting Help

- Check [GitHub Actions Documentation](https://docs.github.com/en/actions)
- Review [Poetry Documentation](https://python-poetry.org/docs/)
- Join our [Discord Community](https://discord.gg/neura)

## Contributing to CI/CD

1. **Adding New Jobs**
   - Create new workflow file
   - Configure triggers
   - Add necessary secrets

2. **Modifying Existing Jobs**
   - Update workflow files
   - Test changes locally
   - Submit pull request

3. **Best Practices**
   - Keep jobs focused
   - Use caching
   - Optimize build times 