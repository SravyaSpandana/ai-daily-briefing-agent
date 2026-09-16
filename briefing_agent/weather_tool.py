import httpx


def get_weather(location: str) -> str:
    """
    Retrieve current weather information for a location.

    Args:
        location: City or location name.

    Returns:
        A formatted weather summary.
    """

    if not location or not location.strip():
        return "Please provide a location."

    encoded_location = location.strip().replace(" ", "+")

    url = f"https://wttr.in/{encoded_location}?format=j1"

    try:
        response = httpx.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "AI-Daily-Briefing-Agent/1.0"
            },
        )

        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]

        temperature = current.get("temp_C", "Unavailable")
        feels_like = current.get("FeelsLikeC", "Unavailable")
        humidity = current.get("humidity", "Unavailable")
        wind_speed = current.get("windspeedKmph", "Unavailable")
        description = current["weatherDesc"][0]["value"]

        return (
            f"Current weather for {location}:\n"
            f"- Condition: {description}\n"
            f"- Temperature: {temperature}°C\n"
            f"- Feels like: {feels_like}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind speed: {wind_speed} km/h"
        )

    except httpx.HTTPError as exc:
        return f"Weather service request failed: {exc}"

    except (KeyError, IndexError, ValueError):
        return "Unable to read the weather service response."

    except Exception as exc:
        return f"Unexpected error while retrieving weather: {exc}"