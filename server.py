#!/usr/bin/env python3
"""
Entry point for the Weather MCP Server
Runs the server with stdio transport
"""

import asyncio
from weather_server import mcp


async def main():
    """Run the MCP server with stdio transport"""
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
