"""MCP client for calling remote tools."""

import httpx
from typing import Dict, Any


async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any], server_url: str = "http://localhost:8002/mcp/") -> str:
    """Call a tool on the MCP server."""
    try:
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                server_url,
                json=request_data,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                }
            )

            if response.status_code == 200:
                result = response.json()
                return result["result"]["content"][0]["text"]
            else:
                return f"HTTP Error: {response.status_code}"

    except Exception as e:
        return f"Tool call failed: {str(e)}"
