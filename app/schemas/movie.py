from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List


class MoviesList(BaseModel):
    title: str
    url: HttpUrl

class MovieData(BaseModel):
    title: str = Field(default=None)
    original_title: Optional[str] = Field(default=None)
    year: Optional[int] = Field(ge=1895, le=2050)
    url: HttpUrl
    slogan: Optional[str] = Field(default=None)
    rating_imdb: Optional[float] = Field(default=None, ge=0, le=10)
    
    genres: List[str] = Field(default=[])
    countries: List[str] = Field(default=[])
    description: Optional[str] = Field(default=None)
    