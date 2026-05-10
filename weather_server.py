#!/usr/bin/env python3
"""
Weather MCP Server using Open-Meteo API
Provides tools to get current weather and forecasts, and resources for available locations.
Supports both stdio and HTTP/SSE transports.
"""

import json
import logging
import httpx
from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the FastMCP server
mcp = FastMCP("weather-server")

# Popular cities with coordinates (latitude, longitude)
CITIES = {
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
    "Paris": {"lat": 48.8566, "lon": 2.3522},
    "Sydney": {"lat": -33.8688, "lon": 151.2093},
    "Dubai": {"lat": 25.2048, "lon": 55.2708},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "San Francisco": {"lat": 37.7749, "lon": -122.4194},
}

OPEN_METEO_BASE = "https://api.open-meteo.com/v1"


@mcp.tool()
async def get_current_weather(city: str) -> str:
    """Get current weather for a specific city.

    Args:
        city: City name (e.g., 'New York', 'London', 'Tokyo'). See available_cities resource for supported cities.
    """
    if city not in CITIES:
        available = ", ".join(CITIES.keys())
        return f"City '{city}' not found. Available cities: {available}"

    coords = CITIES[city]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OPEN_METEO_BASE}/forecast",
                params={
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "current": "temperature_2m,weather_code,wind_speed_10m,apparent_temperature",
                    "timezone": "auto",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            current = data.get("current", {})
            weather_desc = decode_weather_code(current.get("weather_code", 0))

            result = f"""Current Weather in {city}:
Temperature: {current.get("temperature_2m")}°C (feels like {current.get("apparent_temperature")}°C)
Condition: {weather_desc}
Wind Speed: {current.get("wind_speed_10m")} km/h
Timezone: {data.get("timezone", "Unknown")}"""

            return result
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


@mcp.tool()
async def get_forecast(city: str) -> str:
    """Get 7-day weather forecast for a specific city.

    Args:
        city: City name (e.g., 'New York', 'London', 'Tokyo'). See available_cities resource for supported cities.
    """
    if city not in CITIES:
        available = ", ".join(CITIES.keys())
        return f"City '{city}' not found. Available cities: {available}"

    coords = CITIES[city]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OPEN_METEO_BASE}/forecast",
                params={
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum",
                    "timezone": "auto",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            daily = data.get("daily", {})
            times = daily.get("time", [])
            temps_max = daily.get("temperature_2m_max", [])
            temps_min = daily.get("temperature_2m_min", [])
            weather_codes = daily.get("weather_code", [])
            precip = daily.get("precipitation_sum", [])

            forecast_lines = [f"7-Day Forecast for {city}:"]
            for i, date in enumerate(times[:7]):
                weather_desc = decode_weather_code(weather_codes[i])
                forecast_lines.append(
                    f"{date}: {temps_min[i]}°C to {temps_max[i]}°C, {weather_desc}, Precipitation: {precip[i]}mm"
                )

            return "\n".join(forecast_lines)
    except Exception as e:
        return f"Error fetching forecast: {str(e)}"


@mcp.resource("weather://available_cities")
def available_cities() -> str:
    """List of cities with available weather data"""
    cities_data = {
        "cities": [
            {
                "name": city,
                "latitude": coords["lat"],
                "longitude": coords["lon"],
            }
            for city, coords in CITIES.items()
        ]
    }
    return json.dumps(cities_data, indent=2)


def decode_weather_code(code: int) -> str:
    """Convert WMO weather codes to human-readable descriptions."""
    code_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Drizzle (light)",
        53: "Drizzle (moderate)",
        55: "Drizzle (dense)",
        61: "Rain (slight)",
        63: "Rain (moderate)",
        65: "Rain (heavy)",
        71: "Snow (slight)",
        73: "Snow (moderate)",
        75: "Snow (heavy)",
        77: "Snow grains",
        80: "Rain showers (slight)",
        81: "Rain showers (moderate)",
        82: "Rain showers (violent)",
        85: "Snow showers (slight)",
        86: "Snow showers (heavy)",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with hail",
    }
    return code_map.get(code, "Unknown")
