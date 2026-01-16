import logging
from typing import List
from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache

from app.constants import GENRES
from app.schemas.movie import MoviesList, MovieData
from app.core.config import settings
from app.services.parser import parse_films_list, parse_film_details
from app.services.scraper import run_playwright


logger = logging.getLogger("uvicorn.error")

router = APIRouter()

genres = GENRES

@router.get("/")
async def root():
    return {
        "details": "path not implemented. Visit /docs"
    }

@router.get("/genre/{genre_name}", response_model=List[MoviesList])
@cache(expire=settings.cache_expire)
async def get_movies_by_genre(genre_name: str):
    genre_form = genre_name.lower().capitalize()

    if genre_form not in GENRES.keys():
        logger.warning(f"Unsupported genre requested: {genre_name}")
        raise HTTPException(
            status_code=400,
            detail=f"Genre {genre_name} isn`t supported. Available genres: {GENRES.keys()}"
        )
    
    genre_id = GENRES[genre_form]
    url = f"{settings.kinorium_base_url}/R2D2/?order=rating&genres%5B%5D={genre_id}"
    
    logger.info(f"Starting scraping for genre: {genre_form} (ID: {genre_id})")
    
    content, page_url = await run_playwright(
        url=url, 
        headless=True, 
        wait_selector=".filmList"
    )

    if not content:
        logger.error(f"Failed to fetch content from {url}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to load page"
        )
    
    movies = parse_films_list(content)
    logger.info(f"Successfully parsed {len(movies)} movies for genre {genre_form}")
    return movies

@router.get("/movie_details/", response_model=MovieData)
@cache(expire=settings.cache_expire)
async def get_movie_details(title: str = Query(min_length=1)):
    search_url = f"{settings.kinorium_base_url}/search/?q={title}"
    content, film_url = await run_playwright(
        url=search_url,
        headless=True
    )
    
    if not content:
        logger.info(f"Movie '{title}' not found on Kinorium")
        raise HTTPException(
            status_code=404, 
            detail=f"'{title}' not found"
        )
    details = parse_film_details(content, film_url)
    logger.info(f"Successfully parsed details for: {title} (URL: {film_url})")
    return details

@router.get("/open_movie/")
async def get_movie_page(title: str = Query(min_length=1)):
    search_url = f"{settings.kinorium_base_url}/search/?q={title}"
    content, film_url = await run_playwright(
        url=search_url,
        headless=False
    )
    
    if not content:
        logger.info(f"Movie '{title}' not found on Kinorium")
        raise HTTPException(
            status_code=404, 
            detail=f"'{title}' not found"
        )
    logger.info(f"Successfully parsed movie: '{title}' (URL: {film_url})")
    return {"url": film_url}
