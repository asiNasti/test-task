from fastapi import FastAPI, HTTPException

from app.schemas.movie import MovieData, MovieResponse
from parse_film import get_film_data
from parse_genre import get_films


GENRES = {
    "Anime": 1,
    "Biography": 2,
    "Action": 3,
    "Western": 4,
    "War": 5,
    "Game": 11,
    "Detective": 6,
    "Documentary": 9,
    "Drama": 10,
}


app = FastAPI()


@app.get("/movies/{genre_name}", response_model=MovieResponse)
async def get_movies_first(genre_name: str):
    if genre_name not in GENRES.keys():
        raise HTTPException(
            status_code=400,
            detail=f"Genre {genre_name} isn`t supported. Available genres: {GENRES.keys()}"
        )
    
    genre_id = GENRES[genre_name]
    
    try:
        data = await get_films(genre_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/details", response_model=MovieData)
async def get_movies_second(title: str):
    data = await get_film_data(title)
    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Film '{title}' not found!"
        )
    return data