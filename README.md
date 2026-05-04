# Weather MCP Server

A Python Model Context Protocol (MCP) server that provides weather data from the free [Open-Meteo API](https://open-meteo.com/).

## Quick Start

### Setup (one-time)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the Server & Test

**Terminal 1 - Start the Server:**
```bash
cd /Users/somsubhra/somsubhra/mcp-server-demo
source venv/bin/activate
mcp run weather_server.py
```

**Terminal 2 - Start MCP Inspector:**
```bash
cd /Users/somsubhra/somsubhra/mcp-server-demo
npx @modelcontextprotocol/inspector mcp run weather_server.py
```

MCP Inspector opens in your browser. Test the tools and resources there.

## What It Does

### Tools (callable functions)
- **`get_current_weather`** - Get real-time weather for a city
- **`get_forecast`** - Get 7-day weather forecast

### Resources (data sources)
- **`weather://available_cities`** - List of supported cities and coordinates

### Supported Cities
New York, London, Tokyo, Paris, Sydney, Dubai, Singapore, San Francisco

## Project Files

- **`weather_server.py`** - FastMCP server with tools and resources
- **`server.py`** - Entry point for running the server
- **`requirements.txt`** - Python dependencies (mcp, httpx)
- **`SETUP.md`** - Detailed setup and configuration
- **`TESTING.md`** - Testing checklist
- **`EXAMPLES.md`** - Usage examples
- **`.gitignore`** - Git ignore rules

## Testing with MCP Inspector

In the Inspector UI:
1. **Tools tab** → Call `get_current_weather` or `get_forecast` with a city name
2. **Resources tab** → View `weather://available_cities` to see all supported cities

See [TESTING.md](TESTING.md) for detailed test cases.

## Architecture

```
MCP Server
├── Tools (callable by Claude)
│   ├── get_current_weather(city)
│   └── get_forecast(city)
├── Resources (readable by Claude)
│   └── weather://available_cities
└── HTTP Client
    └── Open-Meteo API
```

## Key Features

✅ **No Authentication** - Open-Meteo API is free and open  
✅ **Async/Await** - Fast, non-blocking requests  
✅ **Error Handling** - Graceful handling of invalid inputs  
✅ **Easy Testing** - MCP Inspector for interactive testing  
✅ **Claude Integration** - Works with Claude Desktop app  

## Requirements

- Python 3.11+
- Node.js (for MCP Inspector)
- Internet connection (for weather data)

## Learn More

- [MCP Specification](https://modelcontextprotocol.io/)
- [Open-Meteo API Docs](https://open-meteo.com/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
