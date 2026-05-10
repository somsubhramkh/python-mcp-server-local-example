# Usage Examples - Weather MCP Server

## Setup for Testing

Before running examples, ensure:
1. Server is running: `python server.py` (should show "Uvicorn running on http://0.0.0.0:8000")
2. MCP Inspector is running: `npx @modelcontextprotocol/inspector http://localhost:8000`
3. Browser shows MCP Inspector at the port shown in terminal (e.g., http://localhost:3000 or http://localhost:6274)
   - Check the output of the npx command to find the correct port

## Using MCP Inspector UI

The MCP Inspector provides a browser-based interface to test your MCP server.

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
