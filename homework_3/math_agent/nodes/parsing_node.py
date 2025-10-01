"""Parsing node for ReAct pattern - uses LLM to extract tool calls from reasoning."""

from typing import Dict, Any
from langchain_core.messages import AIMessage
from ..utils.llm import get_llm
from ..state import AgentState


def parsing_node(state: AgentState) -> Dict[str, Any]:
    """
    Parsing node - uses LLM to intelligently extract tool calls from reasoning text.
    This bridges reasoning and action by understanding what the LLM wants to do.
    """
    llm = get_llm()
    messages = state.get("messages", [])
    reasoning = state.get("reasoning", "")

    # Create parsing prompt
    system_prompt = """You are a tool call parser. Your job is to analyze reasoning text and extract exactly what tool should be called with what parameters.

Available tools:
- wolfram_alpha: for complex math, physics formulas, scientific calculations
- calculator: for simple arithmetic expressions
- python_repl: for custom Python code

Read the reasoning text and extract:
1. The tool name (wolfram_alpha, calculator, or python_repl)
2. The exact query/expression/code to pass to that tool

Respond in this EXACT format:
TOOL: [tool_name]
QUERY: [exact_query_to_pass]

If no tool is mentioned, respond with:
TOOL: none
QUERY: none"""

    user_prompt = f"Reasoning text to parse:\n{reasoning}"

    try:
        response = llm.invoke(user_prompt, system_prompt)
        parse_result = response.content

        # Extract tool and query from LLM response
        tool_name = "none"
        query = "none"

        for line in parse_result.split('\n'):
            line = line.strip()
            if line.startswith("TOOL:"):
                tool_name = line.replace("TOOL:", "").strip()
            elif line.startswith("QUERY:"):
                query = line.replace("QUERY:", "").strip()

        # Add parsing result to messages for debugging
        parsing_message = AIMessage(content=f"Parsed tool call: {tool_name} with query: {query}")
        new_messages = messages + [parsing_message]

        return {
            **state,  # Preserve existing state
            "messages": new_messages,
            "tool_name": tool_name,
            "tool_query": query,
            "parse_result": parse_result
        }

    except Exception as e:
        error_msg = f"Parsing error: {str(e)}"
        error_message = AIMessage(content=error_msg)
        new_messages = messages + [error_message]
        return {
            **state,  # Preserve existing state
            "messages": new_messages,
            "tool_name": "none",
            "tool_query": "none",
            "parse_result": error_msg
        }
