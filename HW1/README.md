# OpenAI Tools with Custom Functions - Homework Assignment

This project demonstrates how to use OpenAI's function calling feature with custom tools, including stock data, weather information, and web search capabilities.

## Features

### Available Tools

1. **get_stock_price** - Get current stock prices using Yahoo Finance
2. **get_dividend_date** - Get next dividend payment dates for stocks
3. **get_weather** - Get current weather information for any location
4. **search_web** - Search the web for information using Tavily search API

### Tool Details

#### Stock Tools
- **get_stock_price**: Retrieves real-time stock prices using Yahoo Finance API
- **get_dividend_date**: Gets the next dividend payment date for stocks

#### Weather Tool
The `get_weather` function provides:
- **Automatic location detection**: If no location is specified, it automatically detects your location based on your IP address
- **Manual location input**: You can specify any city and country (e.g., "London, UK", "Tokyo, Japan")
- **Comprehensive weather data**: Temperature, feels like, humidity, weather description, wind speed, and pressure
- **Metric units**: All measurements are in metric units (Celsius, m/s, hPa)
- **Robust fallback system**: Uses OpenWeatherMap API as primary source, with Open-Meteo API as fallback (no API key required)
- **Intelligent geocoding**: Automatically cleans location names for better search results

#### Web Search Tool
The `search_web` function provides:
- **Search types**: Basic (fast) and advanced (comprehensive)
- **Smart query optimization**: Automatically handles news and research queries by modifying search terms
- **Rich results**: Returns title, content preview, URL, and relevance score for each result
- **Configurable results**: Limits results to 5 most relevant items
- **Content preview**: Shows first 300 characters of content with truncation

## Project Structure

```
HW1/
├── tools.py                 # All tool functions and definitions
├── main.py                  # OpenAI integration and main interface
├── test_stocks.py           # Stock tools testing and examples
├── test_weather.py          # Weather tool testing and examples
├── test_web_search.py       # Web search tool testing and examples
├── test_all_tools.py        # Comprehensive testing of all tools
├── README.md                # This documentation
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (create this file)
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (create a `.env` file):
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here  # Required for weather query functionality - 1000 FREE API after registering on openweathermap.org
   TAVILY_API_KEY=your_tavily_api_key_here  # Required for web search functionality - 1000 FREE after registering on tavily.com
   ```

## Usage

### Basic Usage

```python
from main import get_completion_from_messages

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "What's the weather like in Paris?"},
]

response = get_completion_from_messages(messages)
print(response.content)
```

### Standalone Function Usage

```python
from tools import get_stock_price, get_weather, search_web

# Get stock price
stock_info = get_stock_price("MSFT")
print(stock_info)

# Get weather
weather_info = get_weather("London, UK")
print(weather_info)

# Search the web
search_results = search_web("Python programming tutorials")
print(search_results)
```

## Testing

### Individual Tool Tests

Run individual tool tests to verify functionality:

```bash
# Test stock functions
python test_stocks.py

# Test weather function
python test_weather.py

# Test web search function
python test_web_search.py
```

### Comprehensive Testing

Run all tests together:

```bash
python test_all_tools.py
```

### Test Coverage

The test files include:
- **Standalone function testing**: Test each tool independently
- **OpenAI integration testing**: Test tools through function calling
- **Edge case testing**: Test error handling and unusual inputs
- **Performance testing**: Measure response times
- **Tool combination testing**: Test multiple tools working together

## API Dependencies

- **OpenAI API**: Core AI functionality and function calling
- **Yahoo Finance API**: Stock price and dividend data (no API key required)
- **OpenWeatherMap API**: Uses the forecast endpoint (`/forecast`) which provides 5-day weather data in 3-hour intervals. Free tier available, no API key required for basic usage.
- **IP Geolocation**: Uses ipapi.co for IP-based location detection (free tier)
- **Tavily Search API**: Provides web search functionality with multiple search types. Requires API key from [Tavily](https://tavily.com/).

## Error Handling

All tools include comprehensive error handling for:
- Network connectivity issues
- Invalid inputs
- API rate limiting
- Unexpected errors
- Missing API keys

## Example Outputs

### Stock Tool
```json
{
  "ticker": "MSFT",
  "current_price": 420.45
}
```

### Weather Tool
```json
{
  "location": "Tokyo, JP",
  "temperature": "28.0°C",
  "feels_like": "32.4°C",
  "humidity": "83%",
  "description": "broken clouds",
  "wind_speed": "2.6 m/s",
  "pressure": "1013 hPa",
  "forecast_count": 40,
  "next_update": "2025-08-25 21:00:00"
}
```

### Web Search Tool
```json
{
  "query": "artificial intelligence news",
  "search_type": "basic",
  "results_count": 5,
  "results": [
    {
      "title": "Latest AI Breakthroughs in 2024",
      "content": "Recent developments in artificial intelligence have shown remarkable progress...",
      "url": "https://example.com/ai-news",
      "score": 0.95
    }
  ]
}
```

## Notes

- The OpenWeatherMap API free tier has rate limits (60 calls/minute)
- IP geolocation accuracy depends on your network configuration
- All weather data is in metric units for consistency
- The function automatically handles timeouts and network errors gracefully
- Stock data is real-time from Yahoo Finance
- Web search supports both basic and advanced search types

## Homework Requirements

This project demonstrates:
- OpenAI function calling implementation
- Custom tool development
- API integration (multiple external APIs)
- Error handling and edge cases
- Comprehensive testing
- Clean code structure and documentation
- Real-world tool functionality
- Modular design with separation of concerns

## Running the Project

1. **Setup**: Install dependencies and set environment variables
2. **Test**: Run individual or comprehensive tests
3. **Use**: Import functions from `tools.py` or use the AI assistant interface in `main.py`
4. **Extend**: Add new tools following the established pattern in `tools.py`
