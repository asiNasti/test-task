from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ScrapeMethod(str, Enum):
    HTTP = "http"
    HEADLESS = "headless"
    UI = "ui"

class MovieData(BaseModel):
    title: str
    original_title: Optional[str] = Field(default=None)
    year: Optional[int] = Field(ge=1895, le=2050)
    url: HttpUrl
    slogan: Optional[str] = Field(default=None)
    rating_imdb: Optional[float] = Field(default=None, ge=0, le=10)
    
    genres: List[str] = Field(default=[])
    countries: List[str] = Field(default=[])
    duration: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    
class ScrapeResponse(BaseModel):
    data: MovieData
    method: ScrapeMethod
    status: str
    scraped_at: datetime = Field(default_factory=datetime.now)