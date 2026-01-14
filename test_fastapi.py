from fastapi import FastAPI, HTTPException

from parse_genre import get_film_data


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


@app.get("/movies/{genre_name}")
async def get_movies_first(genre_name):
    if genre_name not in GENRES.keys():
        raise HTTPException(
            status_code=400,
            detail=f"Genre {genre_name} isn`t supported. Available genres: {GENRES.keys()}"
        )
    
    genre_id = GENRES[genre_name]
    
    try:
        data = await get_film_data(genre_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))