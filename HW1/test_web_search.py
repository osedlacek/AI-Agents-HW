#!/usr/bin/env python3
"""
Test script for the web search function to verify it works correctly.
This file demonstrates how to use the web search tool both standalone and with OpenAI integration.
"""

import os
from dotenv import load_dotenv
from pprint import pprint

# Import the main functions
from tools import search_web
from main import get_completion_from_messages

# Load environment variables
load_dotenv()

def test_web_search_function_standalone():
    """
    Test the web search function independently without OpenAI integration.
    """
    print("Testing Web Search Function (Standalone)")
    print("=" * 50)
    
    # Test 1: Basic search
    print("\n1. Testing basic search:")
    result1 = search_web("Python programming tutorials")
    print(f"Result: {result1}")
    
    # Test 2: News search
    print("\n2. Testing news search:")
    result2 = search_web("artificial intelligence news", "news")
    print(f"Result: {result2}")
    
    # Test 3: Research search
    print("\n3. Testing research search:")
    result3 = search_web("quantum computing developments 2024", "research")
    print(f"Result: {result3}")
    
    # Test 4: Advanced search
    print("\n4. Testing advanced search:")
    result4 = search_web("machine learning applications", "advanced")
    print(f"Result: {result4}")
    
    # Test 5: Invalid search type
    print("\n5. Testing invalid search type:")
    result5 = search_web("Python tutorials", "invalid_type")
    print(f"Result: {result5}")


def test_web_search_with_openai():
    """
    Test the web search function through OpenAI's function calling system.
    """
    print("\n\nTesting Web Search Tool with OpenAI Integration")
    print("=" * 50)
    
    # Test 1: Basic web search
    print("\n1. Testing basic web search:")
    basic_search_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Search for information about Python programming tutorials"},
    ]
    
    try:
        basic_response = get_completion_from_messages(basic_search_messages)
        print("--- Basic search response: ---")
        pprint(basic_response)
        if hasattr(basic_response, 'content'):
            print("--- Basic search response text: ---")
            print(basic_response.content)
        else:
            print("--- Response type: ---")
            print(type(basic_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: News search
    print("\n2. Testing news search:")
    news_search_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Search for the latest news about artificial intelligence"},
    ]
    
    try:
        news_response = get_completion_from_messages(news_search_messages)
        print("--- News search response: ---")
        pprint(news_response)
        if hasattr(news_response, 'content'):
            print("--- News search response text: ---")
            print(news_response.content)
        else:
            print("--- Response type: ---")
            print(type(news_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Research search
    print("\n3. Testing research search:")
    research_search_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Do a research search about quantum computing developments in 2024"},
    ]
    
    try:
        research_response = get_completion_from_messages(research_search_messages)
        print("--- Research search response: ---")
        pprint(research_response)
        if hasattr(research_response, 'content'):
            print("--- Research response text: ---")
            print(research_response.content)
        else:
            print("--- Response type: ---")
            print(type(research_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Advanced search
    print("\n4. Testing advanced search:")
    advanced_search_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Do an advanced search about machine learning applications in healthcare"},
    ]
    
    try:
        advanced_response = get_completion_from_messages(advanced_search_messages)
        print("--- Advanced search response: ---")
        pprint(advanced_response)
        if hasattr(advanced_response, 'content'):
            print("--- Advanced search response text: ---")
            print(advanced_response.content)
        else:
            print("--- Response type: ---")
            print(type(advanced_response))
    except Exception as e:
        print(f"Error: {e}")


def test_web_search_edge_cases():
    """
    Test edge cases and error handling for the web search function.
    """
    print("\n\nTesting Web Search Edge Cases")
    print("=" * 50)
    
    # Test 1: Empty query
    print("\n1. Testing with empty query:")
    result1 = search_web("")
    print(f"Result: {result1}")
    
    # Test 2: Very long query
    print("\n2. Testing with very long query:")
    long_query = "This is a very long search query that contains many words and might test the limits of the search API and how it handles extremely long input strings that could potentially cause issues with the system"
    result2 = search_web(long_query)
    print(f"Result: {result2}")
    
    # Test 3: Special characters in query
    print("\n3. Testing with special characters in query:")
    special_query = "Python & JavaScript: Best practices for 2024? (Tutorials + Examples)"
    result3 = search_web(special_query)
    print(f"Result: {result3}")
    
    # Test 4: Non-English query
    print("\n4. Testing with non-English query:")
    non_english_query = "Python программирование учебник"
    result4 = search_web(non_english_query)
    print(f"Result: {result4}")


def test_web_search_performance():
    """
    Test the performance and response time of the web search function.
    """
    print("\n\nTesting Web Search Performance")
    print("=" * 50)
    
    import time
    
    # Test 1: Basic search performance
    print("\n1. Testing basic search performance:")
    start_time = time.time()
    result1 = search_web("Python tutorials")
    end_time = time.time()
    print(f"Query: 'Python tutorials'")
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Results count: {result1.get('results_count', 'N/A')}")
    
    # Test 2: Advanced search performance
    print("\n2. Testing advanced search performance:")
    start_time = time.time()
    result2 = search_web("machine learning algorithms", "advanced")
    end_time = time.time()
    print(f"Query: 'machine learning algorithms' (advanced)")
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Results count: {result2.get('results_count', 'N/A')}")
    
    # Test 3: News search performance
    print("\n3. Testing news search performance:")
    start_time = time.time()
    result3 = search_web("AI technology news", "news")
    end_time = time.time()
    print(f"Query: 'AI technology news' (news)")
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Results count: {result3.get('results_count', 'N/A')}")


def main():
    """
    Main function to run all web search tests.
    """
    print("Web Search Function Testing Suite")
    print("=" * 60)
    
    # Check if required environment variables are set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. OpenAI integration tests will fail.")
        print("Set OPENAI_API_KEY in your .env file to test OpenAI integration.")
        print()
    
    if not os.environ.get("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY not set. Web search tests will fail.")
        print("Set TAVILY_API_KEY in your .env file to test web search functionality.")
        print("You can get a free API key from: https://tavily.com/")
        return
    
    # Run standalone tests
    test_web_search_function_standalone()
    
    # Run OpenAI integration tests if API key is available
    if os.environ.get("OPENAI_API_KEY"):
        test_web_search_with_openai()
    else:
        print("\nSkipping OpenAI integration tests due to missing API key.")
    
    # Run edge case tests
    test_web_search_edge_cases()
    
    # Run performance tests
    test_web_search_performance()
    
    print("\n" + "=" * 60)
    print("Web search testing completed!")
    print("Check the results above for any errors or issues.")


if __name__ == "__main__":
    main()
