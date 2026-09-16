from mcp.server.mcpserver import MCPServer

from briefing_agent.finance_tool import get_finance
from briefing_agent.news_tool import get_news
from briefing_agent.weather_tool import get_weather


server = MCPServer("briefing-data-server")


@server.tool()
def news(topic: str) -> str:
    """
    Retrieve recent news headlines for a topic.
    """
    return get_news(topic)


@server.tool()
def weather(location: str) -> str:
    """
    Retrieve current weather information for a location.
    """
    return get_weather(location)


@server.tool()
def finance(symbol: str) -> str:
    """
    Retrieve recent market information for a stock symbol.
    """
    return get_finance(symbol)


if __name__ == "__main__":
    server.run(transport="stdio")