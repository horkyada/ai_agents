"""Reasoning node for ReAct pattern."""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from ..utils.llm import get_llm
from ..state import AgentState


def reasoning_node(state: AgentState) -> Dict[str, Any]:
    """
    Reasoning node - analyzes the problem and decides what to do.
    This is the 'Re' part of ReAct (Reasoning).
    """
    llm = get_llm()
    problem = state.get("problem", "")
    messages = state.get("messages", [])
    iteration = state.get("iteration", 0)

    # Create reasoning prompt
    if iteration == 0:
        # First iteration - understand the problem
        system_prompt = """You are a helpful math and physics tutor.

Analyze the given word problem and decide what tools you need:
- Use 'wolfram_alpha' for complex math, physics formulas, scientific calculations
- Use 'calculator' for simple arithmetic
- Use 'python_repl' for custom calculations or data processing

Think step by step. Respond with your reasoning and what tool you want to use next.
Format: "I need to [action] because [reason]. I will use [tool_name] with query: [specific_query]" """

        user_prompt = f"Problem: {problem}"
    else:
        # Follow-up iterations - analyze previous results
        system_prompt = """Based on the previous tool results, continue your reasoning.

Decide if you need more calculations or if you can provide the final answer.
If you need more tools, specify which one and what query.
If you're ready to answer, say "FINAL_ANSWER:" followed by your complete solution."""

        # Get last few messages for context
        recent_messages = messages[-3:] if len(messages) >= 3 else messages
        context = "\n".join([f"{type(msg).__name__}: {getattr(msg, 'content', str(msg))}" for msg in recent_messages])
        user_prompt = f"Previous context:\n{context}\n\nWhat should I do next?"

    # Get LLM reasoning
    try:
        response = llm.invoke(user_prompt, system_prompt)
        reasoning = response.content

        # Add to messages
        new_messages = messages + [AIMessage(content=reasoning)]

        return {
            **state,  # Preserve existing state
            "messages": new_messages,
            "iteration": iteration + 1,
            "reasoning": reasoning
        }

    except Exception as e:
        error_msg = f"Reasoning error: {str(e)}"
        new_messages = messages + [AIMessage(content=error_msg)]
        return {
            **state,  # Preserve existing state
            "messages": new_messages,
            "iteration": iteration + 1,
            "reasoning": error_msg
        }
