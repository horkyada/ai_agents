import json
import math
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def calculator_tool(operation: str, a: float, b: float = None) -> Dict[str, Any]:
    """
    Calculator tool that performs mathematical operations.
    
    Args:
        operation: The mathematical operation to perform
        a: First number
        b: Second number (optional for single operand operations)
    
    Returns:
        Dictionary with result and operation details
    """
    try:
        if operation == "add" and b is not None:
            result = a + b
        elif operation == "subtract" and b is not None:
            result = a - b
        elif operation == "multiply" and b is not None:
            result = a * b
        elif operation == "divide" and b is not None:
            if b == 0:
                return {"error": "Division by zero is not allowed"}
            result = a / b
        elif operation == "sqrt":
            if a < 0:
                return {"error": "Square root of negative number is not allowed"}
            result = math.sqrt(a)
        elif operation == "power" and b is not None:
            result = a ** b
        elif operation == "abs":
            result = abs(a)
        else:
            return {"error": f"Unknown operation: {operation}"}
        
        return {
            "result": result,
            "operation": operation,
            "operands": [a] + ([b] if b is not None else [])
        }
    except Exception as e:
        return {"error": str(e)}

def process_tool_calls(tool_calls):
    """Process tool calls from the LLM and return results."""
    results = []
    
    for tool_call in tool_calls:
        if tool_call.function.name == "calculator":
            # Parse arguments
            args = json.loads(tool_call.function.arguments)
            
            # Call the calculator tool
            result = calculator_tool(**args)
            
            results.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": "calculator",
                "content": json.dumps(result)
            })
    
    return results

def main():
    # Initialize OpenAI client with Ollama backend
    client = OpenAI(
        api_key="dummy-key",  # Ollama doesn't require real API key
        base_url="http://localhost:11434/v1",  # Ollama's OpenAI-compatible endpoint
    )
    
    # Define the calculator tool for the LLM
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Perform mathematical calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "The mathematical operation to perform",
                            "enum": ["add", "subtract", "multiply", "divide", "sqrt", "power", "abs"]
                        },
                        "a": {
                            "type": "number",
                            "description": "The first number"
                        },
                        "b": {
                            "type": "number",
                            "description": "The second number (optional for single operand operations)"
                        }
                    },
                    "required": ["operation", "a"]
                }
            }
        }
    ]
    
    print("AI Calculator Assistant")
    print("Ask me mathematical questions and I'll use my calculator tool to help!")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            # Initial conversation with the LLM
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant with access to a calculator tool. Use the calculator tool ONLY for mathematical operations like addition, subtraction, multiplication, division, square root, power, and absolute value. For questions that don't require these specific calculations (like age, dates, or general knowledge), answer directly without using tools."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            # First LLM call
            response = client.chat.completions.create(
                model="mistral",  # Using Mistral via Ollama
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            # Check if the LLM wants to use tools
            if response.choices[0].message.tool_calls:
                print("Assistant: Let me calculate that for you...")
                
                # Add the assistant's message to conversation
                messages.append(response.choices[0].message)
                
                # Process tool calls
                tool_results = process_tool_calls(response.choices[0].message.tool_calls)
                
                # Add tool results to messages
                messages.extend(tool_results)
                
                # Get final response from LLM with tool results
                final_response = client.chat.completions.create(
                    model="mistral",
                    messages=messages
                )
                
                print(f"Assistant: {final_response.choices[0].message.content}")
            else:
                # Direct response without tools
                print(f"Assistant: {response.choices[0].message.content}")
                
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure Ollama is running with the 'mistral' model installed.")
            print("Run: ollama pull mistral")

if __name__ == "__main__":
    main()