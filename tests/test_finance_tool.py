import json
from unittest.mock import patch

from briefing_agent.finance_tool import get_finance


def test_get_finance_success():
    fake_finance_response = {
        "chart": {
            "result": [
                {
                    "timestamp": [
                        1726502400,
                        1726588800,
                    ],
                    "indicators": {
                        "quote": [
                            {
                                "open": [198.0, 200.0],
                                "high": [201.0, 203.0],
                                "low": [197.0, 199.0],
                                "close": [199.0, 202.0],
                                "volume": [1000000, 1500000],
                            }
                        ]
                    },
                }
            ]
        }
    }

    with patch("briefing_agent.finance_tool.httpx.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = fake_finance_response
        mock_response.raise_for_status.return_value = None

        result = get_finance("AAPL")

    data = json.loads(result)

    assert data["symbol"] == "AAPL"
    assert data["current_price"] == 202.0
    assert data["previous_close"] == 199.0
    assert data["change"] == 3.0
    assert data["change_percent"] == 3.0 / 199.0 * 100
    assert data["open"] == 200.0
    assert data["day_high"] == 203.0
    assert data["day_low"] == 199.0
    assert data["volume"] == 1500000
    assert data["data_points_retrieved"] == 2


def test_get_finance_empty_symbol():
    result = get_finance("")
    data = json.loads(result)

    assert "error" in data


def test_get_finance_no_market_data():
    fake_finance_response = {
        "chart": {
            "result": []
        }
    }

    with patch("briefing_agent.finance_tool.httpx.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = fake_finance_response
        mock_response.raise_for_status.return_value = None

        result = get_finance("INVALID")

    data = json.loads(result)

    assert "error" in data