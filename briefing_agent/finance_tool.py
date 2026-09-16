import httpx


def get_finance(symbol: str) -> str:
    """
    Retrieve recent market information for a stock symbol.

    Args:
        symbol: Stock ticker symbol, such as AAPL, MSFT, or JPM.

    Returns:
        A formatted market summary.
    """

    if not symbol or not symbol.strip():
        return "Please provide a stock symbol."

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
            return f"No market data found for symbol: {symbol}"

        quote_data = result[0]["indicators"]["quote"][0]
        timestamps = result[0].get("timestamp", [])

        closes = quote_data.get("close", [])
        opens = quote_data.get("open", [])
        highs = quote_data.get("high", [])
        lows = quote_data.get("low", [])
        volumes = quote_data.get("volume", [])

        valid_closes = [
            value for value in closes if value is not None
        ]

        if not valid_closes:
            return f"No closing price data found for symbol: {symbol}"

        latest_close = valid_closes[-1]

        latest_open = next(
            (
                value
                for value in reversed(opens)
                if value is not None
            ),
            "Unavailable",
        )

        latest_high = next(
            (
                value
                for value in reversed(highs)
                if value is not None
            ),
            "Unavailable",
        )

        latest_low = next(
            (
                value
                for value in reversed(lows)
                if value is not None
            ),
            "Unavailable",
        )

        latest_volume = next(
            (
                value
                for value in reversed(volumes)
                if value is not None
            ),
            "Unavailable",
        )

        previous_close = (
            valid_closes[-2]
            if len(valid_closes) >= 2
            else None
        )

        if previous_close is not None:
            change = latest_close - previous_close
            change_percent = (change / previous_close) * 100
            change_text = (
                f"{change:+.2f} "
                f"({change_percent:+.2f}%)"
            )
        else:
            change_text = "Unavailable"

        return (
            f"Recent market data for {symbol}:\n"
            f"- Latest close: {latest_close:.2f}\n"
            f"- Change from previous close: {change_text}\n"
            f"- Open: {latest_open}\n"
            f"- Day high: {latest_high}\n"
            f"- Day low: {latest_low}\n"
            f"- Volume: {latest_volume}\n"
            f"- Data points retrieved: {len(timestamps)}"
        )

    except httpx.HTTPError as exc:
        return f"Finance service request failed: {exc}"

    except (KeyError, IndexError, ValueError, TypeError):
        return "Unable to read the finance service response."

    except Exception as exc:
        return f"Unexpected error while retrieving finance data: {exc}"