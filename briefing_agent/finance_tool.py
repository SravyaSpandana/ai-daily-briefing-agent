import json

import httpx

from briefing_agent.models import FinanceResponse


def get_finance(symbol: str) -> str:
    """
    Retrieve recent market information for a stock symbol.

    Args:
        symbol: Stock ticker symbol, such as AAPL, MSFT, or JPM.

    Returns:
        A JSON string containing recent market information.
    """

    if not symbol or not symbol.strip():
        return json.dumps({
            "symbol": symbol,
            "error": "Please provide a stock symbol.",
        })

    symbol = symbol.strip().upper()

    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{symbol}?range=5d&interval=1d"
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
        data = response.json()

        result = data["chart"]["result"]

        if not result:
            return json.dumps({
                "symbol": symbol,
                "error": f"No market data found for symbol: {symbol}",
            })

        quote_data = result[0]["indicators"]["quote"][0]
        timestamps = result[0].get("timestamp", [])

        closes = quote_data.get("close", [])
        opens = quote_data.get("open", [])
        highs = quote_data.get("high", [])
        lows = quote_data.get("low", [])
        volumes = quote_data.get("volume", [])

        valid_closes = [
            value for value in closes
            if value is not None
        ]

        if not valid_closes:
            return json.dumps({
                "symbol": symbol,
                "error": (
                    f"No closing price data found for symbol: {symbol}"
                ),
            })

        latest_close = valid_closes[-1]

        latest_open = next(
            (
                value
                for value in reversed(opens)
                if value is not None
            ),
            None,
        )

        latest_high = next(
            (
                value
                for value in reversed(highs)
                if value is not None
            ),
            None,
        )

        latest_low = next(
            (
                value
                for value in reversed(lows)
                if value is not None
            ),
            None,
        )

        latest_volume = next(
            (
                value
                for value in reversed(volumes)
                if value is not None
            ),
            None,
        )

        previous_close = (
            valid_closes[-2]
            if len(valid_closes) >= 2
            else None
        )

        if previous_close is not None:
            change = latest_close - previous_close
            change_percent = (change / previous_close) * 100
        else:
            change = None
            change_percent = None

        finance_result = FinanceResponse(
            symbol=symbol,
            company_name=None,
            current_price=float(latest_close),
            previous_close=(
                float(previous_close)
                if previous_close is not None
                else None
            ),
            change=(
                float(change)
                if change is not None
                else None
            ),
            change_percent=(
                float(change_percent)
                if change_percent is not None
                else None
            ),
        )

        result_json = json.loads(
            finance_result.model_dump_json()
        )

        # Include additional market information while preserving
        # the fields defined in the Pydantic model.
        result_json["open"] = latest_open
        result_json["day_high"] = latest_high
        result_json["day_low"] = latest_low
        result_json["volume"] = latest_volume
        result_json["data_points_retrieved"] = len(timestamps)

        return json.dumps(result_json)

    except httpx.HTTPError as exc:
        return json.dumps({
            "symbol": symbol,
            "error": f"Finance service request failed: {str(exc)}",
        })

    except (KeyError, IndexError, ValueError, TypeError):
        return json.dumps({
            "symbol": symbol,
            "error": "Unable to read the finance service response.",
        })

    except Exception as exc:
        return json.dumps({
            "symbol": symbol,
            "error": (
                "Unexpected error while retrieving finance data: "
                f"{str(exc)}"
            ),
        })