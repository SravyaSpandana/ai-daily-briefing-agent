import json
from unittest.mock import patch

from briefing_agent.weather_tool import get_weather


def test_get_weather_success():
    fake_weather_response = {
        "current_condition": [
            {
                "temp_C": "28",
                "FeelsLikeC": "30",
                "humidity": "70",
                "windspeedKmph": "12",
                "weatherDesc": [
                    {
                        "value": "Partly cloudy"
                    }
                ],
            }
        ]
    }

    with patch("briefing_agent.weather_tool.httpx.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = fake_weather_response
        mock_response.raise_for_status.return_value = None

        result = get_weather("Hyderabad")

    data = json.loads(result)

    assert data["location"] == "Hyderabad"
    assert data["temperature"] == "28°C"
    assert data["condition"] == "Partly cloudy"
    assert data["humidity"] == "70%"
    assert data["wind"] == "12 km/h"


def test_get_weather_empty_location():
    result = get_weather("")
    data = json.loads(result)

    assert "error" in data


def test_get_weather_invalid_response():
    with patch("briefing_agent.weather_tool.httpx.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = {}

        result = get_weather("Hyderabad")

    data = json.loads(result)

    assert "error" in data