from briefing_agent.news_tool import get_news
from briefing_agent.weather_tool import get_weather
from briefing_agent.finance_tool import get_finance


def test_news_empty_topic():
    result = get_news("")
    assert "error" in result.lower()


def test_weather_empty_location():
    result = get_weather("")
    assert "error" in result.lower()


def test_finance_empty_symbol():
    result = get_finance("")
    assert "error" in result.lower()