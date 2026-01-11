from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ScrapeMethod(str, Enum):
    HTTP = "http"
    HEADLESS = "headless"
    UI = "ui"

class MovieData(BaseModel):
    title: str = Field(min_length=2, max_length=64)
    original_title: Optional[str] = Field(min_length=2, max_length=64)
    year: Optional[int] = Field(ge=1895, le=2050)
    url: HttpUrl
    rating: Optional[float] = Field(ge=0, le=10)
    votes: Optional[int]
    genres: List[str] = Field(default=[])
    countries: List[str] = Field(default=[])
    director: Optional[str]
    description: Optional[str]
    
class ScrapeResponse(BaseModel):
    data: MovieData
    method: ScrapeMethod
    status: str = Field()
    scraped_at: datetime = Field(default_factory=datetime.now)