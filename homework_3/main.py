"""
Simple ReAct Agent for Math & Physics Word Problems
Using LangGraph + MCP + Wolfram Alpha
"""

import asyncio
from langchain_core.messages import HumanMessage
from math_agent import create_react_graph, AgentState


async def solve_problem(problem: str) -> str:
    """Solve a math or physics word problem."""

    # Create the ReAct graph
    graph = create_react_graph()

    # Initial state
    initial_state = AgentState(
        messages=[HumanMessage(content=problem)],
        iteration=0,
        max_iterations=5,
        problem=problem,
        solution="",
        reasoning="",
        tool_name="",
        tool_query="",
        tool_result="",
        parse_result=""
    )

    print(f"🤔 Problem: {problem}")
    print("🔄 ReAct reasoning...\n")

    try:
        # Run the graph
        final_state = None
        async for event in graph.astream(initial_state):
            for node_name, node_output in event.items():

                if node_name == "reasoning":
                    iteration = node_output.get("iteration", 0)
                    reasoning = node_output.get("reasoning", "")
                    print(f"🧠 Reasoning (step {iteration}): {reasoning[:80]}...")

                elif node_name == "parsing":
                    tool_name = node_output.get("tool_name", "none")
                    tool_query = node_output.get("tool_query", "none")
                    if tool_name != "none":
                        print(f"🔍 Parsing: Found tool '{tool_name}' with query '{tool_query[:50]}...'")

                elif node_name == "action":
                    tool_name = node_output.get("tool_name", "unknown")
                    tool_query = node_output.get("tool_query", "unknown")
                    print(f"🔧 Calling tool {tool_name}: {tool_query[:50]}...")

                    tool_result = node_output.get("tool_result", "")
                    print(f"📥 Result: {tool_result[:80]}...")

                final_state = node_output

        # Extract final answer
        if final_state and final_state.get("messages"):
            for message in reversed(final_state["messages"]):
                content = getattr(message, "content", "")
                if "FINAL_ANSWER:" in content.upper():
                    return content.split("FINAL_ANSWER:")[-1].strip()

            # If no final answer, return last message
            last_message = final_state["messages"][-1]
            return getattr(last_message, "content", "No solution found")

        return "No solution generated"

    except Exception as e:
        return f"Error: {str(e)}"


async def main():
    """Main interactive loop."""
    print("🧮 Math & Physics ReAct Agent")
    print("=" * 40)
    print("💡 Tip: Start the MCP server first:")
    print("   uv run python server.py")
    print("=" * 40)

    # Test problems
    test_problems = [
        "A car travels 120 km in 2 hours. What is its average speed?",
        "What is the kinetic energy of a 2kg ball moving at 5 m/s?",
        "Solve: 3x + 7 = 22",
        "A projectile is fired at 30° with velocity 20 m/s. What's the range?"
    ]

    while True:
        print("\n" + "─" * 40)
        print("Choose an option:")
        for i, problem in enumerate(test_problems, 1):
            print(f"{i}. {problem}")
        print("5: Enter custom problem")
        print("q: Quit")

        try:
            choice = input("\nYour choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if choice.lower() == 'q':
            print("👋 Goodbye!")
            break
        elif choice in ['1', '2', '3', '4']:
            problem = test_problems[int(choice) - 1]
        elif choice == '5':
            problem = input("Enter your problem: ").strip()
            if not problem:
                continue
        else:
            print("Invalid choice!")
            continue

        print("\n" + "=" * 50)
        solution = await solve_problem(problem)
        print(f"\n✅ Solution: {solution}")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
