import logging
import asyncio
import json
from typing import Any

from livekit.agents import function_tool, RunContext
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# try to import DuckDuckGoSearchRun, provide fallback if missing
try:
    from langchain_community.tools import DuckDuckGoSearchRun
except Exception:
    DuckDuckGoSearchRun = None
    logger.warning("langchain_community not installed; search_web will return an error message.")


@function_tool()
async def get_weather(
    context: RunContext,  # type: ignore
    city: str,
) -> str:
    """Get the current weather for a given location (non-blocking)."""
    try:
        def _req():
            return requests.get(f"https://wttr.in/{city}?format=3", timeout=8)

        response = await asyncio.to_thread(_req)
        if response.status_code == 200:
            text = response.text.strip()
            logger.info("Weather for %s: %s", city, text)
            return text
        logger.error("Failed to get weather for %s: %s", city, response.status_code)
        return f"Could not retrieve weather for {city} (status {response.status_code})."
    except Exception as e:
        logger.exception("Error retrieving weather for %s: %s", city, e)
        return f"An error occurred while retrieving weather for {city}."


@function_tool()
async def search_web(
    context: RunContext,  # type: ignore
    query: str,
) -> str:
    """Search the web using DuckDuckGoSearchRun if available, otherwise return a clear message."""
    try:
        if DuckDuckGoSearchRun is None:
            return "Search tool not available: install 'langchain-community' to enable web search."

        search_tool = DuckDuckGoSearchRun()

        if hasattr(search_tool, "arun"):
            results: Any = await search_tool.arun(query)
        else:
            results = await asyncio.to_thread(search_tool.run, query)

        try:
            return json.dumps(results, ensure_ascii=False)
        except TypeError:
            return str(results)
    except Exception as e:
        logger.exception("Error searching the web for '%s': %s", query, e)
        return f"An error occurred while searching the web for '{query}'."


