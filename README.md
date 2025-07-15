# Auto-MCP

Convert any CLI tool for Agentic Use.

## ✨ Overview

This project Auto-MCP is an innovative tool designed to bridge the gap between traditional Command Line Interface (CLI) tools and the emerging interoperability standards for LLMs. The framework is designed to help tool developers to accelerate building extension of their tools to LLMs without having to write a new server, cli or other utility.


### 🎯 The Problem We're Solving

The reason behind creation of this framework is because:

1) **Reusability**: Don't reinvent the wheel when there are APIs or CLIs available.
2) **Maintenance**: Reduces overhead of maintaining a tool service for LLM.

### 🚀 Our Innovative Solution


## 🌟 Key Features

- **Supported Protocols**: 
    - [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
    - [Universal Tool Calling Protocol (UTCP)](https://www.utcp.io) [Future]
    - [Agent2Agent (A2A)](https://github.com/a2aproject/A2A) [Future]
- CLI Tool Aggregator [Future]
- API Support (OpenAPI and Swagger) [Future]


## 🚦 Getting Started

### Pre-requisites

- OpenAI-compliant LLM Service (Mistral Small, Llama 3.3, Granite 3, 8b+ model)
- Python 3

## Environment Setup

```
# Setup virtual environment
pip install uv
uv venv --python 3.9
source .venv/bin/activate

# Install Dependencies
uv pip install -r requirements.txt

# Install automcp
uv pip install -e .
```

## LLM Setup

Create `.env` file: `cp .default_env .env`

Update the following properties in the `.env` file:

- **MODEL_BASE_URL**: OpenAI base url for LLM (/v1 endpoint)
- **MODEL_KEY**: API token for LLM.
- **MODEL_NAME**: Name of the LLM model.

# Usage

```
source .env

# Run automcp
uv run automcp --help

# Generate mcp server for a podman command
mkdir -p tmp
uv run automcp create -p "podman container" -o ./tmp/server.py
```
