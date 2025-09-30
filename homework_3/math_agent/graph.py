"""Simple ReAct graph using LangGraph."""

from typing import Literal
from langgraph.graph import StateGraph
from .state import AgentState
from .nodes.reasoning_node import reasoning_node
from .nodes.parsing_node import parsing_node
from .nodes.action_node import action_node


def should_continue_after_reasoning(state: AgentState) -> Literal["parsing", "end"]:
    """Decide whether to parse for tool calls or end after reasoning."""
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 5)

    # Check iteration limit
    if iteration >= max_iterations:
        return "end"

    # Check if we have a final answer
    messages = state.get("messages", [])
    if messages:
        last_message = messages[-1]
        content = getattr(last_message, "content", "")
        if "FINAL_ANSWER:" in content.upper():
            return "end"

    # Check if reasoning contains a tool call
    reasoning = state.get("reasoning", "")
    if any(tool in reasoning.lower() for tool in ["wolfram", "calculator", "python"]):
        return "parsing"

    # If no tool call and no final answer, end (might be error)
    return "end"


def should_continue_after_parsing(state: AgentState) -> Literal["action", "end"]:
    """Decide whether to take action or end after parsing."""
    tool_name = state.get("tool_name", "none")

    # If parsing found a tool, execute it
    if tool_name != "none" and tool_name:
        return "action"

    # Otherwise, end
    return "end"


def create_react_graph():
    """Create the ReAct graph with reasoning, parsing, and action nodes."""

    # Build graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("reasoning", reasoning_node)
    workflow.add_node("parsing", parsing_node)
    workflow.add_node("action", action_node)

    # Set entry point
    workflow.set_entry_point("reasoning")

    # Add conditional edges
    workflow.add_conditional_edges(
        "reasoning",
        should_continue_after_reasoning,
        {"parsing": "parsing", "end": "__end__"}
    )

    workflow.add_conditional_edges(
        "parsing",
        should_continue_after_parsing,
        {"action": "action", "end": "__end__"}
    )

    # From action, always go back to reasoning
    workflow.add_edge("action", "reasoning")

    return workflow.compile()
