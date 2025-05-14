# Contributing to NEURA

Thank you for your interest in contributing to NEURA! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/neura.git
   cd neura
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Development Workflow

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the coding standards:
   - Use type hints
   - Write docstrings for all functions and classes
   - Follow PEP 8 style guide
   - Write tests for new functionality

3. Run tests and linting:
   ```bash
   poetry run pytest
   poetry run black .
   poetry run isort .
   poetry run mypy .
   poetry run ruff check .
   ```

4. Commit your changes:
   ```bash
   git commit -m "feat: your feature description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Code Standards

- Use Python 3.10+ features
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Write docstrings for all functions and classes
- Write tests for all new functionality
- Keep functions small and focused
- Use meaningful variable and function names

## Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for high test coverage
- Use pytest for testing

## Documentation

- Update README.md if needed
- Add docstrings to all new functions and classes
- Update examples if you add new features
- Document any new environment variables

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation with any new features
3. The PR will be merged once you have the sign-off of at least one maintainer

## Questions?

Feel free to open an issue for any questions or concerns.