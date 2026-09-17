from briefing_agent.models import (
    NewsArticle,
    NewsResponse,
    WeatherResponse,
    FinanceResponse,
)


def test_news_article_model():
    article = NewsArticle(
        title="Test news",
        link="https://example.com",
    )

    assert article.title == "Test news"
    assert article.link == "https://example.com"


def test_news_response_model():
    response = NewsResponse(
        topic="Artificial Intelligence",
        articles=[
            NewsArticle(
                title="AI News",
                link="https://example.com",
            )
        ],
    )

    assert response.topic == "Artificial Intelligence"
    assert len(response.articles) == 1


def test_weather_response_model():
    response = WeatherResponse(
        location="Hyderabad",
        temperature="28°C",
        condition="Clear",
        humidity="70%",
        wind="12 km/h",
    )

    assert response.location == "Hyderabad"
    assert response.temperature == "28°C"
    assert response.condition == "Clear"


def test_finance_response_model():
    response = FinanceResponse(
        symbol="AAPL",
        current_price=200.50,
        previous_close=198.20,
        change=2.30,
        change_percent=1.16,
    )

    assert response.symbol == "AAPL"
    assert response.current_price == 200.50
    assert response.change_percent == 1.16