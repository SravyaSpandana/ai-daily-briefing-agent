from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

import httpx


def get_news(topic: str) -> str:
    """
    Retrieve recent news headlines for a given topic.

    Args:
        topic: The topic to search for.

    Returns:
        A formatted string containing recent news headlines.
    """

    if not topic or not topic.strip():
        return "Please provide a topic to search for news."

    encoded_topic = quote_plus(topic.strip())

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
            return f"No recent news found for the topic: {topic}"

        results = []

        for index, item in enumerate(news_items[:8], start=1):
            title = item.findtext("title") or "Title unavailable"
            published_date = (
                item.findtext("pubDate") or "Publication date unavailable"
            )
            source = item.findtext("source") or "Source unavailable"
            link = item.findtext("link") or "Link unavailable"

            results.append(
                f"{index}. {title}\n"
                f"   Source: {source}\n"
                f"   Published: {published_date}\n"
                f"   Link: {link}"
            )

        return (
            f"Recent news for '{topic}':\n\n"
            + "\n\n".join(results)
        )

    except httpx.HTTPError as exc:
        return f"News service request failed: {exc}"

    except ET.ParseError:
        return "Unable to read the news service response."

    except Exception as exc:
        return f"Unexpected error while retrieving news: {exc}"