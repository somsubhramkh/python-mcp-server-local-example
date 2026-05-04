# Usage Examples - Weather MCP Server

## Using with MCP Inspector

Once you run `mcp dev weather_server.py`, you can interact with the server in the browser-based inspector.

### Example 1: Check Current Weather

1. Open MCP Inspector (browser)
2. Go to **Tools** tab
3. Select **get_current_weather**
4. Enter the parameters:
   ```json
   {
     "city": "New York"
   }
   ```
5. Click **Call tool**

**Expected Response:**
```
Current Weather in New York:
Temperature: 15.2°C (feels like 14.8°C)
Condition: Partly cloudy
Wind Speed: 12 km/h
Humidity: 65%
Timezone: America/New_York
```

### Example 2: Get 7-Day Forecast

1. Go to **Tools** tab
2. Select **get_forecast**
3. Enter:
   ```json
   {
     "city": "London"
   }
   ```
4. Click **Call tool**

**Expected Response:**
```
7-Day Forecast for London:
2026-05-04: 10.5°C to 14.2°C, Partly cloudy, Precipitation: 0mm
2026-05-05: 9.8°C to 13.5°C, Overcast, Precipitation: 2.1mm
2026-05-06: 8.2°C to 12.1°C, Rain (slight), Precipitation: 5.3mm
2026-05-07: 11.1°C to 15.4°C, Mainly clear, Precipitation: 0mm
2026-05-08: 12.5°C to 17.2°C, Clear sky, Precipitation: 0mm
2026-05-09: 10.3°C to 14.8°C, Partly cloudy, Precipitation: 1.2mm
2026-05-10: 9.1°C to 13.5°C, Overcast, Precipitation: 0.5mm
```

### Example 3: View Available Cities

1. Go to **Resources** tab
2. Click on **weather://available_cities**
3. View the resource content

**Expected Response:**
```json
{
  "cities": [
    {
      "name": "New York",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    {
      "name": "London",
      "latitude": 51.5074,
      "longitude": -0.1278
    },
    {
      "name": "Tokyo",
      "latitude": 35.6762,
      "longitude": 139.6503
    },
    {
      "name": "Paris",
      "latitude": 48.8566,
      "longitude": 2.3522
    },
    {
      "name": "Sydney",
      "latitude": -33.8688,
      "longitude": 151.2093
    },
    {
      "name": "Dubai",
      "latitude": 25.2048,
      "longitude": 55.2708
    },
    {
      "name": "Singapore",
      "latitude": 1.3521,
      "longitude": 103.8198
    },
    {
      "name": "San Francisco",
      "latitude": 37.7749,
      "longitude": -122.4194
    }
  ]
}
```

## Using with Claude Desktop

Once integrated in Claude Desktop, you can have natural conversations:

### Example 1: Simple Weather Query
**You:** "What's the weather like in Tokyo right now?"

**Claude:** "Let me check the current weather in Tokyo for you..."
*calls get_current_weather("Tokyo")*

**Claude:** "The current weather in Tokyo is:
- Temperature: 18.5°C (feels like 17.2°C)
- Condition: Partly cloudy
- Wind Speed: 8 km/h
- Humidity: 58%"

### Example 2: Comparing Multiple Cities
**You:** "Compare the weather in Paris and Sydney today."

**Claude:** "I'll check the weather in both cities..."
*calls get_current_weather("Paris") and get_current_weather("Sydney")*

**Claude:** "Here's the comparison:

**Paris:**
- Temperature: 12.3°C (feels like 11.8°C)
- Condition: Overcast
- Wind Speed: 15 km/h
- Humidity: 72%

**Sydney:**
- Temperature: 22.1°C (feels like 21.5°C)
- Condition: Clear sky
- Wind Speed: 10 km/h
- Humidity: 45%

Sydney is much warmer and clearer!"

### Example 3: Planning a Week
**You:** "What's the forecast for London next week? I'm planning a trip."

**Claude:** "Let me get the forecast for you..."
*calls get_forecast("London")*

**Claude:** "Here's the 7-day forecast for London:
- **May 4**: 10-14°C, Partly cloudy, no rain
- **May 5**: 10-13°C, Overcast with 2mm rain
- **May 6**: 8-12°C, Light rain expected, 5mm
- **May 7**: 11-15°C, Clearing up, sunny
- **May 8**: 13-17°C, Beautiful day, clear skies
- **May 9**: 10-15°C, Some clouds, 1mm rain
- **May 10**: 9-13°C, Overcast, minimal precipitation

The best days to visit look like May 7-8!"

### Example 4: Getting a List of Options
**You:** "Which cities can you give me weather for?"

**Claude:** "Let me check what cities I have available..."
*reads weather://available_cities resource*

**Claude:** "I can provide weather data for these 8 cities:
1. New York
2. London
3. Tokyo
4. Paris
5. Sydney
6. Dubai
7. Singapore
8. San Francisco

Pick any of these, and I can get you current weather or a forecast!"

## Error Handling Examples

### Example: Invalid City
**In MCP Inspector:**
```json
{
  "city": "Atlantis"
}
```

**Response:**
```
City 'Atlantis' not found. Available cities: New York, London, Tokyo, Paris, Sydney, Dubai, Singapore, San Francisco
```

### Example: Empty City Name
**In MCP Inspector:**
```json
{
  "city": ""
}
```

**Response:**
```
City '' not found. Available cities: New York, London, Tokyo, Paris, Sydney, Dubai, Singapore, San Francisco
```

## Debugging Tips

### View Server Logs
While MCP Inspector runs, check the terminal for logs:
```
[INFO] Tool called: get_current_weather
[INFO] Fetching weather for: New York
[DEBUG] API request to open-meteo.com...
[DEBUG] Response status: 200
```

### Check Network Activity
In MCP Inspector or browser DevTools:
1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Look for requests to `api.open-meteo.com`
4. Each tool call should trigger an HTTP request
5. Verify responses are HTTP 200

### Test Different Scenarios
Try these tool calls to understand behavior:

| Input | Expected Behavior |
|-------|-------------------|
| `{"city": "New York"}` | Returns current weather |
| `{"city": "new york"}` | Case sensitive - may fail (try "New York") |
| `{"city": "NYC"}` | Not found - requires full name |
| `{"city": " London "}` | Whitespace is trimmed, should work |

## Integration Checklist

- [ ] MCP Inspector shows "weather-server" connected
- [ ] Can call get_current_weather for any supported city
- [ ] Can call get_forecast for any supported city
- [ ] Can read weather://available_cities resource
- [ ] Response times are < 2-3 seconds
- [ ] No errors in server logs
- [ ] Claude Desktop recognizes the server (if set up)
- [ ] Can have natural conversations about weather

## Performance Notes

- **First request**: May take 1-2 seconds (DNS lookup + API call)
- **Subsequent requests**: Usually < 1 second
- **Timeout**: 10 seconds per request to Open-Meteo API
- **Concurrent requests**: Server handles multiple simultaneous requests
