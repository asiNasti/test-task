from typing import List
from fastapi import APIRouter, HTTPException

from app.constants import GENRES
from app.schemas.movie import MoviesList, MovieData
from app.core.config import settings
from app.services.parser import parse_films_list, parse_film_details
from app.services.scraper import run_playwright

router = APIRouter()

genres = GENRES

@router.get("/genre/{genre_name}", response_model=List[MoviesList])
async def get_movies_by_genre(genre_name: str):
    if genre_name.lower().capitalize() not in GENRES.keys():
        raise HTTPException(
            status_code=400,
            detail=f"Genre {genre_name} isn`t supported. Available genres: {GENRES.keys()}"
        )
    
    genre_id = GENRES[genre_name.lower().capitalize()]
    url = f"{settings.kinorium_base_url}/R2D2/?order=rating&genres%5B%5D={genre_id}"
    
    content, page_url = await run_playwright(
        url=url, 
        headless=True, 
        wait_selector=".filmList"
    )

    if not content:
        raise HTTPException(
            status_code=500, 
            detail="Failed to load page"
        )
 
    return parse_films_list(content)

@router.get("/movie_details/", response_model=MovieData)
async def get_movie_details(title: str):
    search_url = f"{settings.kinorium_base_url}/search/?q={title}"
    
    content, film_url = await run_playwright(
        url=search_url,
        headless=True
    )
    
    if not content:
        raise HTTPException(
            status_code=404, 
            detail=f"'{title}' not found"
        )
        
    return parse_film_details(content, film_url)

@router.get("/open_movie/")
async def get_movie_page(title: str):
    search_url = f"{settings.kinorium_base_url}/search/?q={title}"
    
    content, film_url = await run_playwright(
        url=search_url,
        headless=False
    )
    
    if not content:
        raise HTTPException(
            status_code=404, 
            detail=f"'{title}' not found"
        )
        
    return {"url": film_url}
