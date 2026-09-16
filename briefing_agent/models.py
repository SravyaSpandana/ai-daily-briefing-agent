from typing import List, Optional
from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    title: str
    link: str
    published: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None


class NewsResponse(BaseModel):
    topic: str
    articles: List[NewsArticle] = Field(default_factory=list)


class WeatherResponse(BaseModel):
    location: str
    temperature: Optional[str] = None
    condition: Optional[str] = None
    humidity: Optional[str] = None
    wind: Optional[str] = None
    forecast: Optional[str] = None


class FinanceResponse(BaseModel):
    symbol: str
    company_name: Optional[str] = None
    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None


class DailyBriefing(BaseModel):
    news: List[NewsArticle] = Field(default_factory=list)
    weather: Optional[WeatherResponse] = None
    finance: List[FinanceResponse] = Field(default_factory=list)