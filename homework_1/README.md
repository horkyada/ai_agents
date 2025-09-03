# Homework 1: LLM API with Calculator Tool

This project demonstrates calling an LLM API that uses a tool (calculator function) and returns the response back to the LLM.

## Assignment Requirements

✅ **Calls LLM API**: Uses Ollama via OpenAI-compatible interface  
✅ **Uses a tool**: Calculator tool for mathematical operations  
✅ **Returns response to LLM**: Tool results are fed back to LLM for final response  

## Features

- **LLM Backend**: Ollama (local, no API costs)
- **Interface**: OpenAI-compatible API via Ollama
- **Tool**: Calculator with operations: add, subtract, multiply, divide, sqrt, power, abs
- **Interactive**: Chat-based interface for testing

## Prerequisites

1. **Install Ollama**: https://ollama.ai
2. **Install a model**:
   ```bash
   ollama pull mistral
   ```
3. **Start Ollama** (if not running as service):
   ```bash
   ollama serve
   ```

## Installation

```bash
cd homework_1
uv sync
```

## Usage

```bash
uv run main.py
```

## Example Interactions

```
You: What is 15 + 27?
Assistant: Let me calculate that for you...
Assistant: 15 + 27 equals 42.

You: What's the square root of 144?
Assistant: Let me calculate that for you...
Assistant: The square root of 144 is 12.

You: Calculate 2 to the power of 8
Assistant: Let me calculate that for you...
Assistant: 2 raised to the power of 8 equals 256.
```

## How It Works

1. User asks a mathematical question
2. LLM recognizes it needs the calculator tool
3. Script calls the appropriate calculator function
4. Tool result is returned to the LLM
5. LLM provides final formatted response to user

## Configuration

Copy `.env.example` to `.env` and adjust settings if needed:

```bash
cp .env.example .env
```