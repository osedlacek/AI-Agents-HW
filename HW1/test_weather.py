#!/usr/bin/env python3
"""
Test script for the weather function to verify it works correctly.
This file demonstrates how to use the weather tool both standalone and with OpenAI integration.
"""

import os
from dotenv import load_dotenv
import requests
from pprint import pprint

# Import the main functions
from tools import get_weather
from main import get_completion_from_messages

# Load environment variables
load_dotenv()

def test_weather_function_standalone():
    """
    Test the weather function independently without OpenAI integration.
    """
    print("Testing Weather Function (Standalone)")
    print("=" * 50)
    
    # Test 1: Specific location
    print("\n1. Testing with specific location (London, UK):")
    result1 = get_weather("London, UK")
    print(f"Result: {result1}")
    
    # Test 2: IP-based location detection
    print("\n2. Testing IP-based location detection:")
    result2 = get_weather()
    print(f"Result: {result2}")
    
    # Test 3: Another specific location
    print("\n3. Testing with another location (Tokyo, Japan):")
    result3 = get_weather("Tokyo, Japan")
    print(f"Result: {result3}")
    
    # Test 4: Invalid location
    print("\n4. Testing with invalid location:")
    result4 = get_weather("InvalidCity123, XX")
    print(f"Result: {result4}")


def test_weather_with_openai():
    """
    Test the weather function through OpenAI's function calling system.
    """
    print("\n\nTesting Weather Tool with OpenAI Integration")
    print("=" * 50)
    
    # Test 1: Weather for specific location
    print("\n1. Testing weather for specific location (Paris, France):")
    weather_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What's the weather like in Paris, France?"},
    ]
    
    try:
        weather_response = get_completion_from_messages(weather_messages)
        print("--- Weather response: ---")
        pprint(weather_response)
        if hasattr(weather_response, 'content'):
            print("--- Weather response text: ---")
            print(weather_response.content)
        else:
            print("--- Response type: ---")
            print(type(weather_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: IP-based location detection
    print("\n2. Testing IP-based location detection:")
    ip_weather_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What's the weather like where I am?"},
    ]
    
    try:
        ip_weather_response = get_completion_from_messages(ip_weather_messages)
        print("--- IP-based weather response: ---")
        pprint(ip_weather_response)
        if hasattr(ip_weather_response, 'content'):
            print("--- IP-based weather response text: ---")
            print(ip_weather_response.content)
        else:
            print("--- Response type: ---")
            print(type(ip_weather_response))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Weather comparison
    print("\n3. Testing weather comparison (New York vs London):")
    comparison_messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Compare the weather in New York and London right now."},
    ]
    
    try:
        comparison_response = get_completion_from_messages(comparison_messages)
        print("--- Weather comparison response: ---")
        pprint(comparison_response)
        if hasattr(comparison_response, 'content'):
            print("--- Weather comparison response text: ---")
            print(comparison_response.content)
        else:
            print("--- Response type: ---")
            print(type(comparison_response))
    except Exception as e:
        print(f"Error: {e}")


def test_weather_edge_cases():
    """
    Test edge cases and error handling for the weather function.
    """
    print("\n\nTesting Weather Edge Cases")
    print("=" * 50)
    
    # Test 1: Empty string location
    print("\n1. Testing with empty string location:")
    result1 = get_weather("")
    print(f"Result: {result1}")
    
    # Test 2: Very long location name
    print("\n2. Testing with very long location name:")
    long_location = "A very long city name that might cause issues with the API call and should be handled gracefully by the system"
    result2 = get_weather(long_location)
    print(f"Result: {result2}")
    
    # Test 3: Special characters in location
    print("\n3. Testing with special characters in location:")
    special_location = "São Paulo, Brasil"
    result3 = get_weather(special_location)
    print(f"Result: {result3}")


def main():
    """
    Main function to run all weather tests.
    """
    print("Weather Function Testing Suite")
    print("=" * 60)
    
    # Check if required environment variables are set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. OpenAI integration tests will fail.")
        print("Set OPENAI_API_KEY in your .env file to test OpenAI integration.")
        print()
    
    if not os.environ.get("OPENWEATHER_API_KEY"):
        print("Note: OPENWEATHER_API_KEY not set. Using free tier of OpenWeatherMap API.")
        print()
    
    # Run standalone tests
    test_weather_function_standalone()
    
    # Run OpenAI integration tests if API key is available
    if os.environ.get("OPENAI_API_KEY"):
        test_weather_with_openai()
    else:
        print("\nSkipping OpenAI integration tests due to missing API key.")
    
    # Run edge case tests
    test_weather_edge_cases()
    
    print("\n" + "=" * 60)
    print("Weather testing completed!")
    print("Check the results above for any errors or issues.")


if __name__ == "__main__":
    main()
