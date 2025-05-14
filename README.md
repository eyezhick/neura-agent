# 🧠 NEURA - Neural Entity for Understanding, Reasoning, and Autonomy

NEURA is a cutting-edge LLM-powered agent framework that simulates autonomous reasoning and task execution across multiple environments. Built with LangGraph and modern AI technologies, NEURA provides a robust foundation for creating intelligent, autonomous agents.

## 🌟 Features

- 🤖 **Multi-Modal Agent Framework**: Support for web, CLI, API, and local knowledge base interactions
- 🧩 **Modular Architecture**: Easily plug in different LLMs, memory modules, and tools
- 🔄 **Autonomous Reasoning**: Task decomposition and planning capabilities
- 📚 **Memory Management**: Vector DB and file-based memory for long-term learning
- 🔌 **Extensible Environment Support**: Operate in local, cloud, or hybrid environments
- 🤝 **Multi-Agent Coordination**: Support for agent composition and collaboration
- 📊 **Rich CLI**: Beautiful command-line interface with progress tracking and formatted output
- 🎯 **Task Planning**: Sophisticated planning capabilities for complex task decomposition
- 📝 **Memory Management**: Persistent storage and retrieval of past interactions

## 🏗️ Architecture

```
neura/
├── agents/           # Core agent implementations
│   ├── base.py      # Base agent class
│   ├── planner.py   # Planning agent
│   └── executor.py  # Task execution agent
├── core/            # Core framework components
│   ├── memory/      # Memory management
│   ├── tools/       # Tool implementations
│   └── graph/       # LangGraph workflow definitions
├── environments/    # Environment implementations
│   ├── web/        # Web interaction
│   ├── cli/        # CLI interaction
│   └── api/        # API interaction
├── memory/         # Memory implementations
│   ├── vector/     # Vector DB integration
│   └── file/       # File-based memory
└── utils/          # Utility functions
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Poetry (for dependency management)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/neura.git
cd neura
```

2. Install dependencies:
```bash
poetry install
```

3. Install Playwright browsers:
```bash
poetry run playwright install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Quick Start

```python
from neura.agents import PlannerAgent, ExecutorAgent
from neura.core.graph import create_agent_graph

# Create agent graph
graph = create_agent_graph(
    planner=PlannerAgent(),
    executor=ExecutorAgent()
)

# Run the agent
result = graph.run("Research the latest developments in quantum computing")
```

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- [Architecture Overview](docs/architecture.md)
- [Agent Development Guide](docs/agent-development.md)
- [Environment Integration](docs/environments.md)
- [Memory Management](docs/memory.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LangGraph for the powerful agent workflow framework
- LangChain for the excellent LLM integration tools
- The open-source AI community for inspiration and support
- Playwright for web automation
- Typer for CLI development
- Rich for beautiful terminal output

## 📊 CLI Usage

NEURA provides a powerful CLI for executing tasks and managing memory:

```bash
# Execute a task
neura run "Research the latest developments in quantum computing"

# Execute with custom parameters
neura run "Analyze the impact of AI on healthcare" --model gpt-4 --temperature 0.8 --max-steps 10

# Search memories
neura memory --query "quantum computing"

# View memory statistics
neura memory

# Clear all memories
neura memory --clear
```

## 🐛 Bug Reports

If you encounter any bugs or issues, please report them by opening an issue on the GitHub repository.
