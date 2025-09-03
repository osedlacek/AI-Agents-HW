#!/usr/bin/env python3
"""
Comprehensive test runner for all OpenAI tools.
This file demonstrates how to use all tools together and provides integration testing.
"""

import os
from dotenv import load_dotenv
from pprint import pprint

# Import the main functions
from tools import (
    get_stock_price, 
    get_dividend_date, 
    get_weather, 
    search_web
)
from main import get_completion_from_messages

# Load environment variables
load_dotenv()

def test_all_tools_standalone():
    """
    Test all tools independently without OpenAI integration.
    """
    print("Testing All Tools (Standalone)")
    print("=" * 60)
    
    # Test Stock Tools
    print("\n--- STOCK TOOLS ---")
    print("1. Stock price for MSFT:")
    stock_result = get_stock_price("MSFT")
    print(f"   Result: {stock_result}")
    
    print("2. Dividend date for MSFT:")
    dividend_result = get_dividend_date("MSFT")
    print(f"   Result: {dividend_result}")
    
    # Test Weather Tool
    print("\n--- WEATHER TOOL ---")
    print("3. Weather for Tokyo:")
    weather_result = get_weather("Tokyo, Japan")
    print(f"   Result: {weather_result}")
    
    # Test Web Search Tool
    print("\n--- WEB SEARCH TOOL ---")
    print("4. Web search for Python tutorials:")
    search_result = search_web("Python programming tutorials")
    print(f"   Result: {search_result}")


def test_all_tools_with_openai():
    """
    Test all tools through OpenAI's function calling system.
    """
    print("\n\nTesting All Tools with OpenAI Integration")
    print("=" * 60)
    
    # Test 1: Multi-tool query (stocks and weather)
    print("\n1. Testing multi-tool query (stocks and weather):")
    multi_tool_messages = [
        {"role": "system", "content": "You are a helpful AI assistant with access to stock, weather, and web search tools."},
        {"role": "user", "content": "Get the current stock price for Microsoft and tell me the weather in London. Also search for the latest news about artificial intelligence."},
    ]
    
    try:
        multi_tool_response = get_completion_from_messages(multi_tool_messages)
        print("--- Multi-tool response: ---")
        pprint(multi_tool_response)
        if hasattr(multi_tool_response, 'content'):
            print("--- Multi-tool response text: ---")
            print(multi_tool_response.content)
        else:
            print("--- Response type: ---")
            print(type(multi_tool_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Financial analysis with weather context
    print("\n2. Testing financial analysis with weather context:")
    financial_weather_messages = [
        {"role": "system", "content": "You are a financial analyst AI assistant."},
        {"role": "user", "content": "Analyze the stock prices of Microsoft, Google, and Apple. Also check the weather in New York and search for any weather-related market impacts."},
    ]
    
    try:
        financial_weather_response = get_completion_from_messages(financial_weather_messages)
        print("--- Financial weather response: ---")
        pprint(financial_weather_response)
        if hasattr(financial_weather_response, 'content'):
            print("--- Financial weather response text: ---")
            print(financial_weather_response.content)
        else:
            print("--- Response type: ---")
            print(type(financial_weather_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Research and analysis
    print("\n3. Testing research and analysis:")
    research_messages = [
        {"role": "system", "content": "You are a research AI assistant."},
        {"role": "user", "content": "Research the latest developments in quantum computing, get the current stock price of IBM, and check the weather in San Francisco. Provide a comprehensive analysis."},
    ]
    
    try:
        research_response = get_completion_from_messages(research_messages)
        print("--- Research response: ---")
        pprint(research_response)
        if hasattr(research_response, 'content'):
            print("--- Research response text: ---")
            print(research_response.content)
        else:
            print("--- Response type: ---")
            print(type(research_response))
    except Exception as e:
        print(f"Error: {e}")


def test_tool_combinations():
    """
    Test specific combinations of tools to ensure they work together.
    """
    print("\n\nTesting Tool Combinations")
    print("=" * 60)
    
    # Test 1: Stocks + Weather
    print("\n1. Testing Stocks + Weather combination:")
    stocks_weather_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Get the stock prices of Tesla and check the weather in Los Angeles. Are there any weather conditions that might affect Tesla's operations?"},
    ]
    
    try:
        response = get_completion_from_messages(stocks_weather_messages)
        print("--- Stocks + Weather response: ---")
        pprint(response)
        if hasattr(response, 'content'):
            print("--- Response text: ---")
            print(response.content)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Web Search + Stocks
    print("\n2. Testing Web Search + Stocks combination:")
    search_stocks_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Search for the latest news about electric vehicles and get the current stock prices of Tesla and Ford. Provide market insights."},
    ]
    
    try:
        response = get_completion_from_messages(search_stocks_messages)
        print("--- Web Search + Stocks response: ---")
        pprint(response)
        if hasattr(response, 'content'):
            print("--- Response text: ---")
            print(response.content)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Weather + Web Search
    print("\n3. Testing Weather + Web Search combination:")
    weather_search_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Check the weather in Miami and search for any travel advisories or weather warnings for that area."},
    ]
    
    try:
        response = get_completion_from_messages(weather_search_messages)
        print("--- Weather + Web Search response: ---")
        pprint(response)
        if hasattr(response, 'content'):
            print("--- Response text: ---")
            print(response.content)
    except Exception as e:
        print(f"Error: {e}")


def test_error_handling():
    """
    Test error handling across all tools.
    """
    print("\n\nTesting Error Handling")
    print("=" * 60)
    
    # Test 1: Invalid stock ticker
    print("\n1. Testing invalid stock ticker:")
    invalid_stock_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Get the stock price for INVALID123"},
    ]
    
    try:
        response = get_completion_from_messages(invalid_stock_messages)
        print("--- Invalid stock response: ---")
        pprint(response)
        if hasattr(response, 'content'):
            print("--- Response text: ---")
            print(response.content)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Invalid location
    print("\n2. Testing invalid location:")
    invalid_location_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Get the weather for InvalidCity123, XX"},
    ]
    
    try:
        response = get_completion_from_messages(invalid_location_messages)
        print("--- Invalid location response: ---")
        pprint(response)
        if hasattr(response, 'content'):
            print("--- Response text: ---")
            print(response.content)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Complex query with potential errors
    print("\n3. Testing complex query with potential errors:")
    complex_error_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Get the stock price for MSFT, weather for London, and search for information about quantum computing. Also try to get the stock price for INVALID and weather for FAKECITY."},
    ]
    
    try:
        response = get_completion_from_messages(complex_error_messages)
        print("--- Complex error response: ---")
        pprint(response)
        if hasattr(response, 'content'):
            print("--- Response text: ---")
            print(response.content)
    except Exception as e:
        print(f"Error: {e}")


def main():
    """
    Main function to run all comprehensive tests.
    """
    print("OpenAI Tools Comprehensive Testing Suite")
    print("=" * 80)
    
    # Check if required environment variables are set
    missing_keys = []
    if not os.environ.get("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
        print("Warning: OPENAI_API_KEY not set. OpenAI integration tests will fail.")
    
    if not os.environ.get("TAVILY_API_KEY"):
        missing_keys.append("TAVILY_API_KEY")
        print("Warning: TAVILY_API_KEY not set. Web search tests will fail.")
    
    if not os.environ.get("OPENWEATHER_API_KEY"):
        print("Note: OPENWEATHER_API_KEY not set. Using free tier of OpenWeatherMap API.")
    
    if missing_keys:
        print(f"\nSet the following environment variables in your .env file:")
        for key in missing_keys:
            print(f"  {key}")
        print()
    
    # Run standalone tests
    test_all_tools_standalone()
    
    # Run OpenAI integration tests if API key is available
    if os.environ.get("OPENAI_API_KEY"):
        test_all_tools_with_openai()
        test_tool_combinations()
        test_error_handling()
    else:
        print("\nSkipping OpenAI integration tests due to missing API key.")
    
    print("\n" + "=" * 80)
    print("Comprehensive testing completed!")
    print("Check the results above for any errors or issues.")
    print("\nTo run individual tool tests:")
    print("  python test_stocks.py      # Test stock functions")
    print("  python test_weather.py     # Test weather function")
    print("  python test_web_search.py  # Test web search function")
    print("  python test_all_tools.py   # Test all tools together")


if __name__ == "__main__":
    main()
