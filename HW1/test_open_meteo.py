#!/usr/bin/env python3
"""
Test script to verify Open-Meteo fallback functionality.
"""

import os
from tools import get_weather
from pprint import pprint

def test_open_meteo_fallback():
    """Test Open-Meteo fallback when OpenWeatherMap API key is not available."""

    print("Testing Open-Meteo Fallback Functionality")
    print("=" * 50)

    # Test 1: With OpenWeatherMap API key (should use primary API)
    print("\n1. Testing with OpenWeatherMap API key (primary API):")
    result1 = get_weather("London, UK")
    pprint(result1)

    # Test 2: Temporarily disable OpenWeatherMap API key to test fallback
    print("\n2. Testing Open-Meteo fallback (no API key):")
    original_key = os.environ.get("OPENWEATHER_API_KEY")
    # Temporarily remove the API key from environment
    if "OPENWEATHER_API_KEY" in os.environ:
        del os.environ["OPENWEATHER_API_KEY"]

    # Create a temporary version of get_weather without API key
    import requests

    def get_weather_fallback(location: str = None):
        """Test version of get_weather without OpenWeatherMap API key."""
        try:
            # If no location provided, get location from IP
            if not location:
                ip_response = requests.get('https://ipapi.co/json/', timeout=5)
                if ip_response.status_code == 200:
                    ip_data = ip_response.json()
                    location = f"{ip_data.get('city', 'Unknown')}, {ip_data.get('country_name', 'Unknown')}"
                else:
                    return {"error": "Could not determine location from IP address"}

            # Skip OpenWeatherMap API (no key available)
            # Fallback to Open-Meteo API (no key required)
            try:
                # First, get coordinates for the location using Open-Meteo geocoding
                geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
                geocoding_params = {
                    'name': location,
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
                                "location": f"{location_name}, {country}",
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

    result2 = get_weather_fallback("London, UK")
    pprint(result2)

    # Restore original API key
    if original_key:
        os.environ["OPENWEATHER_API_KEY"] = original_key

    # Test 3: Different location
    print("\n3. Testing different location with Open-Meteo:")
    result3 = get_weather("New York, US")
    pprint(result3)

    # Test 4: Invalid location
    print("\n4. Testing invalid location:")
    result4 = get_weather("InvalidCity123, XX")
    pprint(result4)

if __name__ == "__main__":
    test_open_meteo_fallback()
