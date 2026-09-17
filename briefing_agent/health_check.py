from typing import Dict

import httpx


def check_news_service() -> bool:
    """
    Check whether Google News RSS is reachable.
    """

    try:
        response = httpx.get(
            "https://news.google.com/rss/search?q=technology",
            timeout=5,
            headers={
                "User-Agent": "AI-Daily-Briefing-Agent/1.0"
            },
        )

        return response.status_code == 200

    except httpx.HTTPError:
        return False


def check_weather_service() -> bool:
    """
    Check whether wttr.in is reachable.
    """

    try:
        response = httpx.get(
            "https://wttr.in/Hyderabad?format=j1",
            timeout=5,
            headers={
                "User-Agent": "AI-Daily-Briefing-Agent/1.0"
            },
        )

        return response.status_code == 200

    except httpx.HTTPError:
        return False


def check_finance_service() -> bool:
    """
    Check whether Yahoo Finance is reachable.
    """

    try:
        response = httpx.get(
            "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
            "?range=1d&interval=1d",
            timeout=5,
            headers={
                "User-Agent": "AI-Daily-Briefing-Agent/1.0"
            },
        )

        return response.status_code == 200

    except httpx.HTTPError:
        return False


def get_service_health() -> Dict[str, bool]:
    """
    Return the availability status of all external services.
    """

    return {
        "news_service": check_news_service(),
        "weather_service": check_weather_service(),
        "finance_service": check_finance_service(),
    }