from urllib.parse import quote_plus
import xml.etree.ElementTree as ET
import json

import httpx
import logging

from briefing_agent.models import NewsArticle, NewsResponse

logger = logging.getLogger(__name__)
def get_news(topic: str) -> str:
    """
    Retrieve recent news headlines for a given topic.

    Args:
        topic: The topic to search for.

    Returns:
        A JSON string containing recent news headlines.
    """
    logger.info("Fetching news for topic: %s", topic)
    if not topic or not topic.strip():
        return json.dumps({
            "topic": topic,
            "articles": [],
            "error": "Please provide a topic to search for news.",
        })

    topic = topic.strip()
    encoded_topic = quote_plus(topic)

    url = (
        f"https://news.google.com/rss/search?"
        f"q={encoded_topic}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    try:
        response = httpx.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "AI-Daily-Briefing-Agent/1.0"
            },
        )

        response.raise_for_status()

        root = ET.fromstring(response.text)
        news_items = root.findall("./channel/item")

        if not news_items:
            result = NewsResponse(
                topic=topic,
                articles=[],
            )

            return result.model_dump_json()

        articles = []

        for item in news_items[:8]:
            title = item.findtext("title") or "Title unavailable"
            published_date = (
                item.findtext("pubDate")
                or "Publication date unavailable"
            )
            source = item.findtext("source") or "Source unavailable"
            link = item.findtext("link") or "Link unavailable"

            article = NewsArticle(
                title=title,
                link=link,
                published=published_date,
                source=source,
            )

            articles.append(article)
            logger.info("News API request succeeded for topic: %s", topic)

        result = NewsResponse(
            topic=topic,
            articles=articles,
        )

        return result.model_dump_json()

    except httpx.HTTPError as exc:
        logger.exception("News API request failed for topic: %s", topic)
        return json.dumps({
            "topic": topic,
            "articles": [],
            "error": f"News service request failed: {str(exc)}",
        })

    except ET.ParseError:
        logger.exception("Unable to parse news response for topic: %s", topic)
        return json.dumps({
            "topic": topic,
            "articles": [],
            "error": "Unable to read the news service response.",
        })

    except Exception as exc:
        logger.exception(
        "Unexpected error while retrieving news for topic: %s",
        topic,
    )
        return json.dumps({
            "topic": topic,
            "articles": [],
            "error": (
                f"Unexpected error while retrieving news: {str(exc)}"
            ),
        })