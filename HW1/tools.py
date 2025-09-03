
"""
OpenAI Tools Module
Contains all the custom tool functions for OpenAI function calling.
"""

import os
import yfinance as yf
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Tavily client only if API key is available
tavily_client = None
try:
    from tavily import TavilyClient
    if os.environ.get("TAVILY_API_KEY"):
        tavily_client = TavilyClient(
            api_key=os.environ.get("TAVILY_API_KEY"),
        )
except ImportError:
    pass

def get_stock_price(ticker: str):
    """
    Get current stock price using Yahoo Finance API.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'MSFT', 'GOOG')
    
    Returns:
        dict: Dictionary containing ticker and current price
    """
    if not ticker or not ticker.strip():
        return {"error": "Ticker symbol cannot be empty"}
    
    try:
        ticker_info = yf.Ticker(ticker).info
        current_price = ticker_info.get("currentPrice")
        return {"ticker": ticker, "current_price": current_price}
    except Exception as e:
        return {"error": f"Failed to get stock price for {ticker}: {str(e)}"}


def get_dividend_date(ticker: str):
    """
    Get next dividend payment date for a stock using Yahoo Finance API.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'MSFT', 'GOOG')
    
    Returns:
        dict: Dictionary containing ticker and dividend date
    """
    if not ticker or not ticker.strip():
        return {"error": "Ticker symbol cannot be empty"}
    
    try:
        ticker_info = yf.Ticker(ticker).info
        dividend_date = ticker_info.get("dividendDate")
        return {"ticker": ticker, "dividend_date": dividend_date}
    except Exception as e:
        return {"error": f"Failed to get dividend date for {ticker}: {str(e)}"}


def get_weather(location: str = None):
    """
    Get current weather for a location. If no location is provided, 
    uses IP-based geolocation to determine the caller's location.
    Uses OpenWeatherMap API with Open-Meteo API as fallback (no key required).
    
    Args:
        location (str, optional): The city and country for weather information
    
    Returns:
        dict: Dictionary containing weather information
    """
    try:
        # If no location provided, get location from IP
        if not location:
            ip_response = requests.get('https://ipapi.co/json/', timeout=5)
            if ip_response.status_code == 200:
                ip_data = ip_response.json()
                location = f"{ip_data.get('city', 'Unknown')}, {ip_data.get('country_name', 'Unknown')}"
            else:
                return {"error": "Could not determine location from IP address"}
        
        # Try OpenWeatherMap API first (if API key is available)
        openweather_api_key = os.environ.get("OPENWEATHER_API_KEY")
        if openweather_api_key:
            try:
                weather_url = "https://api.openweathermap.org/data/2.5/forecast"
                params = {
                    'q': location,
                    'units': 'metric',  # Use Celsius
                    'appid': openweather_api_key
                }
                
                weather_response = requests.get(weather_url, params=params, timeout=10)
                
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    
                    # Get current weather (first entry in the list)
                    current_weather = weather_data['list'][0]
                    
                    return {
                        "location": f"{weather_data['city']['name']}, {weather_data['city']['country']}",
                        "temperature": f"{current_weather['main']['temp']:.1f}°C",
                        "feels_like": f"{current_weather['main']['feels_like']:.1f}°C",
                        "humidity": f"{current_weather['main']['humidity']}%",
                        "description": current_weather['weather'][0]['description'],
                        "wind_speed": f"{current_weather['wind']['speed']} m/s",
                        "pressure": f"{current_weather['main']['pressure']} hPa",
                        "forecast_count": weather_data['cnt'],
                        "next_update": current_weather['dt_txt'],
                        "source": "OpenWeatherMap"
                    }
            except Exception as e:
                print(f"OpenWeatherMap API failed, trying Open-Meteo fallback: {str(e)}")

        # Fallback to Open-Meteo API (no key required)
        try:
            # First, get coordinates for the location using Open-Meteo geocoding
            # Clean the location name by removing country suffix for better geocoding
            search_location = location.split(',')[0].strip() if ',' in location else location

            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            geocoding_params = {
                'name': search_location,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }

            geocoding_response = requests.get(geocoding_url, params=geocoding_params, timeout=10)
            
            if geocoding_response.status_code == 200:
                geocoding_data = geocoding_response.json()
                
                if geocoding_data.get('results'):
                    result = geocoding_data['results'][0]
                    lat = result['latitude']
                    lon = result['longitude']
                    location_name = result['name']
                    country = result.get('country', 'Unknown')
                    
                    # Get weather data using coordinates
                    weather_url = "https://api.open-meteo.com/v1/forecast"
                    weather_params = {
                        'latitude': lat,
                        'longitude': lon,
                        'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code',
                        'hourly': 'temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code',
                        'timezone': 'auto'
                    }
                    
                    weather_response = requests.get(weather_url, params=weather_params, timeout=10)
                    
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        
                        # Get current weather
                        current = weather_data['current']
                        
                        # Convert weather code to description
                        weather_codes = {
                            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                            45: "Foggy", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
                            55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
                            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
                            66: "Light freezing rain", 67: "Heavy freezing rain", 71: "Slight snow fall",
                            73: "Moderate snow fall", 75: "Heavy snow fall", 77: "Snow grains",
                            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
                            85: "Slight snow showers", 86: "Heavy snow showers", 95: "Thunderstorm",
                            96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
                        }
                        
                        weather_description = weather_codes.get(current['weather_code'], "Unknown")

                        return {
                            "location": location,  # Use original location format
                            "temperature": f"{current['temperature_2m']:.1f}°C",
                            "feels_like": f"{current['apparent_temperature']:.1f}°C",
                            "humidity": f"{current['relative_humidity_2m']}%",
                            "description": weather_description,
                            "wind_speed": f"{current['wind_speed_10m']} km/h",
                            "pressure": f"{current['pressure_msl']:.0f} hPa",
                            "forecast_count": len(weather_data.get('hourly', {}).get('time', [])),
                            "next_update": weather_data['current']['time'],
                            "source": "Open-Meteo"
                        }
                    else:
                        return {"error": f"Open-Meteo weather API failed. Status: {weather_response.status_code}"}
                else:
                    return {"error": f"Could not find coordinates for location: {location}"}
            else:
                return {"error": f"Open-Meteo geocoding API failed. Status: {geocoding_response.status_code}"}
                
        except Exception as e:
            return {"error": f"Open-Meteo API error: {str(e)}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def search_web(query: str, search_type: str = "basic"):
    """
    Search the web using Tavily search API.
    
    Args:
        query (str): The search query
        search_type (str): Type of search - "basic" (fast) or "advanced" (comprehensive)
    
    Returns:
        dict: Search results with title, content, and URL
    """
    if not tavily_client:
        return {"error": "Tavily API key not configured. Please set TAVILY_API_KEY environment variable."}
    
    try:
        # Validate search type - Tavily only supports basic and advanced
        valid_types = ["basic", "advanced"]
        if search_type not in valid_types:
            search_type = "basic"
        
        # For news searches, modify the query to include news-specific terms
        if search_type == "news" or "news" in query.lower():
            query = f"{query} news"
            search_type = "basic"  # Use basic for news searches
        
        # For research searches, use advanced depth
        if search_type == "research":
            search_type = "advanced"
        
        # Perform the search
        search_result = tavily_client.search(
            query=query,
            search_depth=search_type,
            include_domains=[],
            exclude_domains=[],
            max_results=5
        )
        
        if search_result and 'results' in search_result:
            # Format the results
            formatted_results = []
            for result in search_result['results'][:5]:  # Limit to 5 results
                formatted_results.append({
                    "title": result.get('title', 'No title'),
                    "content": result.get('content', 'No content')[:300] + "..." if len(result.get('content', '')) > 300 else result.get('content', 'No content'),
                    "url": result.get('url', 'No URL'),
                    "score": result.get('score', 0)
                })
            
            return {
                "query": query,
                "search_type": search_type,
                "results_count": len(formatted_results),
                "results": formatted_results
            }
        else:
            return {"error": "No search results found"}
            
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}


# Define custom tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Use this function to get the current price of a stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The ticker symbol for the stock, e.g. GOOG",
                    }
                },
                "required": ["ticker"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_dividend_date",
            "description": "Use this function to get the next dividend payment date of a stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The ticker symbol for the stock, e.g. GOOG",
                    }
                },
                "required": ["ticker"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather information for a specific location. If no location is provided, automatically detects the caller's location based on IP address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country for weather information (e.g., 'London,UK'). If not provided, will use IP-based geolocation.",
                    }
                },
                "required": [],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information using Tavily search API. Supports basic (fast) and advanced (comprehensive) search types. News and research queries are automatically optimized.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on the web",
                    },
                    "search_type": {
                        "type": "string",
                        "description": "Type of search: 'basic' (fast) or 'advanced' (comprehensive). News and research queries are automatically handled. Defaults to 'basic'.",
                        "enum": ["basic", "advanced"]
                    }
                },
                "required": ["query"],
            },
        }
    },
]


available_functions = {
    "get_stock_price": get_stock_price,
    "get_dividend_date": get_dividend_date,
    "get_weather": get_weather,
    "search_web": search_web,
}
