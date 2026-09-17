import json
from unittest.mock import patch

from briefing_agent.news_tool import get_news


def test_get_news_success():
    fake_rss_response = """
    <rss>
        <channel>
            <item>
                <title>AI Technology Update</title>
                <link>https://example.com/ai-news</link>
                <pubDate>Wed, 17 Sep 2026 10:00:00 GMT</pubDate>
                <source>Example News</source>
            </item>
        </channel>
    </rss>
    """

    with patch("briefing_agent.news_tool.httpx.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.text = fake_rss_response
        mock_response.raise_for_status.return_value = None

        result = get_news("artificial intelligence")

    data = json.loads(result)

    assert data["topic"] == "artificial intelligence"
    assert len(data["articles"]) == 1
    assert data["articles"][0]["title"] == "AI Technology Update"


def test_get_news_empty_topic():
    result = get_news("")
    data = json.loads(result)

    assert data["articles"] == []
    assert "error" in data


def test_get_news_no_results():
    fake_rss_response = """
    <rss>
        <channel>
        </channel>
    </rss>
    """

    with patch("briefing_agent.news_tool.httpx.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.text = fake_rss_response
        mock_response.raise_for_status.return_value = None

        result = get_news("unknown-topic")

    data = json.loads(result)

    assert data["topic"] == "unknown-topic"
    assert data["articles"] == []