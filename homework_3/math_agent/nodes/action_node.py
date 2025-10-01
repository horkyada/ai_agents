"""Action node for ReAct pattern."""

from typing import Dict, Any
from langchain_core.messages import ToolMessage
from ..utils.mcp_client import call_mcp_tool
from ..state import AgentState


async def action_node(state: AgentState) -> Dict[str, Any]:
    """
    Action node - executes tools based on parsed results.
    This is the 'Act' part of ReAct (Acting).
    """
    messages = state.get("messages", [])
    tool_name = state.get("tool_name", "none")
    query = state.get("tool_query", "none")

    if tool_name == "none" or not tool_name:
        # No tool call found, return error
        error_msg = "No valid tool call found after parsing"
        new_messages = messages + [ToolMessage(content=error_msg, tool_call_id="error")]
        return {
            **state,  # Preserve existing state
            "messages": new_messages,
            "tool_result": error_msg
        }

    # Call the MCP tool
    try:
        if tool_name == "wolfram_alpha":
            result = await call_mcp_tool("wolfram_alpha", {"query": query})
        elif tool_name == "calculator":
            result = await call_mcp_tool("calculator", {"expression": query})
        elif tool_name == "python_repl":
            result = await call_mcp_tool("python_repl", {"code": query})
        else:
            result = f"Unknown tool: {tool_name}"

        # Add tool result to messages
        tool_message = ToolMessage(content=f"Tool {tool_name} result: {result}", tool_call_id=tool_name)
        new_messages = messages + [tool_message]

        return {
            **state,  # Preserve existing state
            "messages": new_messages,
            "tool_result": result
        }

    except Exception as e:
        error_msg = f"Tool execution error: {str(e)}"
        tool_message = ToolMessage(content=error_msg, tool_call_id="error")
        new_messages = messages + [tool_message]
        return {
            **state,  # Preserve existing state
            "messages": new_messages,
            "tool_result": error_msg
        }
