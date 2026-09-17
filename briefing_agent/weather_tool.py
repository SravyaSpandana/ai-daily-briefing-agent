import json

import httpx

from briefing_agent.models import WeatherResponse


def get_weather(location: str) -> str:
    """
    Retrieve current weather information for a location.

    Args:
        location: City or location name.

    Returns:
        A JSON string containing current weather information.
    """

    if not location or not location.strip():
        return json.dumps({
            "location": location,
            "error": "Please provide a location.",
        })

    location = location.strip()
    encoded_location = location.replace(" ", "+")

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

        temperature = current.get("temp_C")
        feels_like = current.get("FeelsLikeC")
        humidity = current.get("humidity")
        wind_speed = current.get("windspeedKmph")

        weather_description = current.get("weatherDesc", [{}])[0]
        description = weather_description.get(
            "value",
            "Condition unavailable",
        )

        result = WeatherResponse(
            location=location,
            temperature=(
                f"{temperature}°C"
                if temperature is not None
                else "Unavailable"
            ),
            condition=description,
            humidity=(
                f"{humidity}%"
                if humidity is not None
                else "Unavailable"
            ),
            wind=(
                f"{wind_speed} km/h"
                if wind_speed is not None
                else "Unavailable"
            ),
            forecast=(
                f"Feels like {feels_like}°C"
                if feels_like is not None
                else None
            ),
        )

        return result.model_dump_json()

    except httpx.HTTPError as exc:
        return json.dumps({
            "location": location,
            "error": f"Weather service request failed: {str(exc)}",
        })

    except (KeyError, IndexError, ValueError, TypeError):
        return json.dumps({
            "location": location,
            "error": "Unable to read the weather service response.",
        })

    except Exception as exc:
        return json.dumps({
            "location": location,
            "error": (
                f"Unexpected error while retrieving weather: {str(exc)}"
            ),
        })