#!/usr/bin/env python3
"""
Test script for the stock functions to verify they work correctly.
This file demonstrates how to use the stock tools both standalone and with OpenAI integration.
"""

import os
from dotenv import load_dotenv
from pprint import pprint

# Import the main functions
from tools import get_stock_price, get_dividend_date
from main import get_completion_from_messages

# Load environment variables
load_dotenv()

def test_stock_functions_standalone():
    """
    Test the stock functions independently without OpenAI integration.
    """
    print("Testing Stock Functions (Standalone)")
    print("=" * 50)
    
    # Test 1: Get stock price for MSFT
    print("\n1. Testing stock price for MSFT:")
    result1 = get_stock_price("MSFT")
    print(f"Result: {result1}")
    
    # Test 2: Get stock price for GOOG
    print("\n2. Testing stock price for GOOG:")
    result2 = get_stock_price("GOOG")
    print(f"Result: {result2}")
    
    # Test 3: Get stock price for AAPL
    print("\n3. Testing stock price for AAPL:")
    result3 = get_stock_price("AAPL")
    print(f"Result: {result3}")
    
    # Test 4: Get dividend date for MSFT
    print("\n4. Testing dividend date for MSFT:")
    result4 = get_dividend_date("MSFT")
    print(f"Result: {result4}")
    
    # Test 5: Get dividend date for GOOG
    print("\n5. Testing dividend date for GOOG:")
    result5 = get_dividend_date("GOOG")
    print(f"Result: {result5}")
    
    # Test 6: Invalid ticker symbol
    print("\n6. Testing invalid ticker symbol:")
    result6 = get_stock_price("INVALID123")
    print(f"Result: {result6}")


def test_stock_functions_with_openai():
    """
    Test the stock functions through OpenAI's function calling system.
    """
    print("\n\nTesting Stock Tools with OpenAI Integration")
    print("=" * 50)
    
    # Test 1: Get stock price
    print("\n1. Testing stock price query:")
    stock_price_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is the current stock price for Microsoft (MSFT)?"},
    ]
    
    try:
        stock_price_response = get_completion_from_messages(stock_price_messages)
        print("--- Stock price response: ---")
        pprint(stock_price_response)
        if hasattr(stock_price_response, 'content'):
            print("--- Stock price response text: ---")
            print(stock_price_response.content)
        else:
            print("--- Response type: ---")
            print(type(stock_price_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Get dividend date
    print("\n2. Testing dividend date query:")
    dividend_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "When is the next dividend payment date for Microsoft (MSFT)?"},
    ]
    
    try:
        dividend_response = get_completion_from_messages(dividend_messages)
        print("--- Dividend date response: ---")
        pprint(dividend_response)
        if hasattr(dividend_response, 'content'):
            print("--- Dividend date response text: ---")
            print(dividend_response.content)
        else:
            print("--- Response type: ---")
            print(type(dividend_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Compare multiple stocks
    print("\n3. Testing multiple stock comparison:")
    comparison_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Compare the current stock prices of Microsoft (MSFT), Google (GOOG), and Apple (AAPL)"},
    ]
    
    try:
        comparison_response = get_completion_from_messages(comparison_messages)
        print("--- Stock comparison response: ---")
        pprint(comparison_response)
        if hasattr(comparison_response, 'content'):
            print("--- Stock comparison response text: ---")
            print(comparison_response.content)
        else:
            print("--- Response type: ---")
            print(type(comparison_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Stock analysis request
    print("\n4. Testing stock analysis request:")
    analysis_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Get the stock price and dividend information for Tesla (TSLA)"},
    ]
    
    try:
        analysis_response = get_completion_from_messages(analysis_messages)
        print("--- Stock analysis response: ---")
        pprint(analysis_response)
        if hasattr(analysis_response, 'content'):
            print("--- Stock analysis response text: ---")
            print(analysis_response.content)
        else:
            print("--- Response type: ---")
            print(type(analysis_response))
    except Exception as e:
        print(f"Error: {e}")


def test_stock_functions_edge_cases():
    """
    Test edge cases and error handling for the stock functions.
    """
    print("\n\nTesting Stock Functions Edge Cases")
    print("=" * 50)
    
    # Test 1: Empty ticker symbol
    print("\n1. Testing with empty ticker symbol:")
    result1 = get_stock_price("")
    print(f"Result: {result1}")
    
    # Test 2: Very long ticker symbol
    print("\n2. Testing with very long ticker symbol:")
    long_ticker = "A" * 100
    result2 = get_stock_price(long_ticker)
    print(f"Result: {result2}")
    
    # Test 3: Special characters in ticker
    print("\n3. Testing with special characters in ticker:")
    special_ticker = "MS-FT@123"
    result3 = get_stock_price(special_ticker)
    print(f"Result: {result3}")
    
    # Test 4: Non-existent ticker
    print("\n4. Testing with non-existent ticker:")
    fake_ticker = "FAKE123"
    result4 = get_stock_price(fake_ticker)
    print(f"Result: {result4}")


def test_stock_functions_performance():
    """
    Test the performance and response time of the stock functions.
    """
    print("\n\nTesting Stock Functions Performance")
    print("=" * 50)
    
    import time
    
    # Test 1: Stock price performance
    print("\n1. Testing stock price performance:")
    start_time = time.time()
    result1 = get_stock_price("MSFT")
    end_time = time.time()
    print(f"Query: MSFT stock price")
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Result: {result1}")
    
    # Test 2: Dividend date performance
    print("\n2. Testing dividend date performance:")
    start_time = time.time()
    result2 = get_dividend_date("GOOG")
    end_time = time.time()
    print(f"Query: GOOG dividend date")
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Result: {result2}")
    
    # Test 3: Multiple stock queries performance
    print("\n3. Testing multiple stock queries performance:")
    tickers = ["MSFT", "GOOG", "AAPL", "TSLA", "AMZN"]
    start_time = time.time()
    results = []
    for ticker in tickers:
        try:
            result = get_stock_price(ticker)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e)})
    end_time = time.time()
    print(f"Queries: {len(tickers)} stock prices")
    print(f"Total response time: {end_time - start_time:.2f} seconds")
    print(f"Average time per query: {(end_time - start_time) / len(tickers):.2f} seconds")
    for i, result in enumerate(results):
        print(f"  {tickers[i]}: {result}")


def main():
    """
    Main function to run all stock function tests.
    """
    print("Stock Functions Testing Suite")
    print("=" * 60)
    
    # Check if required environment variables are set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. OpenAI integration tests will fail.")
        print("Set OPENAI_API_KEY in your .env file to test OpenAI integration.")
        print()
    
    # Run standalone tests
    test_stock_functions_standalone()
    
    # Run OpenAI integration tests if API key is available
    if os.environ.get("OPENAI_API_KEY"):
        test_stock_functions_with_openai()
    else:
        print("\nSkipping OpenAI integration tests due to missing API key.")
    
    # Run edge case tests
    test_stock_functions_edge_cases()
    
    # Run performance tests
    test_stock_functions_performance()
    
    print("\n" + "=" * 60)
    print("Stock functions testing completed!")
    print("Check the results above for any errors or issues.")


if __name__ == "__main__":
    main()
