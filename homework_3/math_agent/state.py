"""Agent state definition."""

from typing import List, Any, Dict
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State for the ReAct math agent."""
    messages: List[Any]
    iteration: int
    max_iterations: int
    problem: str
    solution: str
    reasoning: str
    tool_name: str
    tool_query: str
    tool_result: str
    parse_result: str
