import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Import tools from the tools module
from tools import (
    get_stock_price,
    get_dividend_date, 
    get_weather,
    search_web,
    tools,
    available_functions
)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_completion_from_messages(messages, model="gpt-4o"):
    """
    Process messages and handle function calls using OpenAI's function calling feature.
    
    Args:
        messages (list): List of message dictionaries with role and content
        model (str): OpenAI model to use (default: "gpt-4o")
    
    Returns:
        OpenAI message object or error string
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,  # Custom tools
        tool_choice="auto"  # Allow AI to decide if a tool should be called
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        # Find the tool call content
        tool_call = response_message.tool_calls[0]

        # Extract tool name and arguments
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments) 
        tool_id = tool_call.id
        
        # Call the function
        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)

        messages.append({
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tool_id,  
                    "type": "function",
                    "function": {
                        "name": function_name,
                        "arguments": json.dumps(function_args),
                    }
                }
            ]
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_id,  
            "name": function_name,
            "content": json.dumps(function_response),
        })

        # Second call to get final response based on function output
        second_response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,  
            tool_choice="auto"  
        )
        final_answer = second_response.choices[0].message

        return final_answer

    return "No relevant function call found."


def main():
    """
    Main function to demonstrate the OpenAI tools functionality.
    This function can be used for basic testing or as a starting point.
    """
    print("OpenAI Tools with Custom Functions")
    print("=" * 50)
    print("Available tools:")
    print("1. get_stock_price - Get stock prices")
    print("2. get_dividend_date - Get dividend dates")
    print("3. get_weather - Get weather information")
    print("4. search_web - Search the web")
    print("\nUse the get_completion_from_messages() function to interact with the AI assistant.")
    print("See test files for examples of how to use each tool.")


if __name__ == "__main__":
    main()
