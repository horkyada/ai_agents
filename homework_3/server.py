import asyncio
import logging
import os
from typing import Any, Callable, Dict, List, Optional
import contextlib
from collections.abc import AsyncIterator
import uvicorn

# MCP
from mcp.server.lowlevel import Server
import mcp.types as types
from mcp.server.lowlevel.helper_types import ReadResourceContents

from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send

# Import tool implementations
from tools.calculator import calculate
from tools.python_repl import execute_python
from tools.wolfram import wolfram_query

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("mcp-tools-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available tools with their schemas."""
    return [
        types.Tool(
            name="calculator",
            description="Perform mathematical calculations using Python expressions",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)')",
                    }
                },
                "required": ["expression"],
            },
        ),
        types.Tool(
            name="python_repl",
            description="Execute Python code in an isolated environment",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute",
                    }
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="wolfram_alpha",
            description="Query Wolfram Alpha for computational knowledge",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query for Wolfram Alpha (e.g., 'population of France', 'integrate x^2')",
                    }
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Optional[Dict[str, Any]] = None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if arguments is None:
        arguments = {}

    try:
        if name == "calculator":
            result = await calculate(arguments.get("expression", ""))
            return [types.TextContent(type="text", text=str(result))]

        elif name == "python_repl":
            output = await execute_python(arguments.get("code", ""))
            return [types.TextContent(type="text", text=output)]

        elif name == "wolfram_alpha":
            result = await wolfram_query(arguments.get("query", ""))
            return [types.TextContent(type="text", text=result)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        error_msg = f"Tool execution error: {str(e)}"
        logger.error(error_msg)
        return [types.TextContent(type="text", text=error_msg)]


# ---------------------------------
# SSE Server Transport
# ---------------------------------

# Create the session manager with our app and event store
session_manager = StreamableHTTPSessionManager(
    app=server,
    json_response=True,  # Use JSON responses
    event_store=None,  # No resumability
    stateless=True,
)


# ASGI handler for streamable HTTP connections
async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
    await session_manager.handle_request(scope, receive, send)


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    """Context manager for managing session manager lifecycle."""
    async with session_manager.run():
        print("Application started with StreamableHTTP session manager!")
        try:
            yield
        finally:
            print("Application shutting down...")


starlette_app = Starlette(
    debug=True,
    routes=[
        Mount("/mcp", app=handle_streamable_http),
    ],
    lifespan=lifespan,
)

if __name__ == "__main__":
    try:
        print("Starting MCP tools server...")
        # Run the server
        uvicorn.run(starlette_app, host="0.0.0.0", port=8002)
    except KeyboardInterrupt:
        print("Server stopped by user.")
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise e
