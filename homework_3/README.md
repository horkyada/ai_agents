# Math & Physics ReAct Agent

ReAct agent for solving math and physics word problems using:
- **LangGraph**: Custom ReAct implementation
- **MCP**: Tool server with calculator, Python REPL, and Wolfram Alpha
- **LiteLLM**: Local model support

## Architecture

The agent implements a ReAct pattern with three nodes:
1. **Reasoning Node**: Analyzes problems and decides on actions
2. **Parsing Node**: Extracts tool calls from reasoning text using LLM
3. **Action Node**: Executes tools via MCP server

Flow: reasoning → parsing → action → back to reasoning (until final answer)

## Available Tools

### **calculator**
- **Description**: Mathematical calculations using Python expressions
- **Input**: `expression` (string) - Expression to evaluate
- **Example**: `{"expression": "2 + 2"}` or `{"expression": "sqrt(16)"}`

### **python_repl**
- **Description**: Execute Python code in a controlled environment
- **Input**: `code` (string) - Python code to execute
- **Example**: `{"code": "import math; print(math.pi)"}`

### **wolfram_alpha**
- **Description**: Query Wolfram Alpha for computational knowledge
- **Input**: `query` (string) - Query for Wolfram Alpha
- **Requires**: `WOLFRAM_APP_ID` environment variable
- **Example**: `{"query": "integrate x^2 dx"}`

## Project Structure

```
homework_3/
├── README.md           # This file
├── main.py             # ReAct agent entry point
├── server.py           # MCP server
├── pyproject.toml      # Dependencies
├── math_agent/         # ReAct implementation
│   ├── __init__.py
│   ├── graph.py        # LangGraph workflow
│   ├── state.py        # Agent state definition
│   ├── nodes/          # ReAct nodes
│   │   ├── reasoning_node.py
│   │   ├── parsing_node.py
│   │   └── action_node.py
│   └── utils/          # Utilities
│       ├── llm.py      # LiteLLM setup
│       └── mcp_client.py
└── tools/              # MCP tools
    ├── calculator.py
    ├── python_repl.py
    └── wolfram.py
```

## Usage

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys:
# LITELLM_MODEL=ollama/mistral:latest
# WOLFRAM_APP_ID=your_wolfram_app_id
```

### 2. Start MCP Server

```bash
uv run python server.py
```

### 3. Run Agent

```bash
uv run python main.py
```

The agent provides 4 test problems plus custom input option.

## Test Problems

1. "A car travels 120 km in 2 hours. What is its average speed?"
2. "What is the kinetic energy of a 2kg ball moving at 5 m/s?"
3. "Solve: 3x + 7 = 22"
4. "A projectile is fired at 30° with velocity 20 m/s. What's the range?"
