from typing import List
from bs4 import BeautifulSoup
from ..schemas.movie import MovieData, MoviesList
from ..core.config import settings


def parse_films_list(content: str) -> List[MoviesList]:
    soup = BeautifulSoup(content, "html.parser")

    films_data = []
    films = soup.select('.filmList__item-wrap-title')
    for film in films:
        title_el = film.select_one(".movie-title__text .title")
        link_el = film.select_one("a")
        
        if title_el and link_el:
            title = title_el.get_text(strip=True).replace('\xa0', ' ')
            url = f"{settings.kinorium_base_url}{link_el['href']}"
            films_data.append(MoviesList(title=title, url=url))

    return films_data



def parse_film_details(content: str, film_url: str) -> MovieData:
    soup = BeautifulSoup(content, "html.parser")
    title = soup.select_one(".film-page__title-text")
    orig_title = soup.select_one(".film-page__orig_with_comment")
    year = soup.select_one(".film-page__date a")
    slogan = soup.select_one(".film-page__slogan")
    rating = soup.select_one(".ratingsBlockIMDbKP span")
    genres = [el.get_text(strip=True) for el in soup.find_all("li", itemprop="genre")]
    countries = [el.get_text(strip=True) for el in soup.select(".film-page__country-links a")]

    #sep function
    desc_el = soup.select_one(".film-page__text")
    if desc_el:
        if desc_el.h2:
            desc_el.h2.decompose() 
        description = desc_el.get_text(strip=True).replace('\xa0', ' ')
    else:
        description = None

    return MovieData(
        title=title.get_text(strip=True) if title else None,
        url=film_url,
        original_title=orig_title.get_text(strip=True) if orig_title else None,
        year=int(year.get_text(strip=True)) if year else None,
        slogan=slogan.get_text(strip=True).strip("«»").replace('\xa0', ' ') if slogan else None,
        rating_imdb=float(rating.get_text(strip=True)) if rating else None,
        genres=genres,
        countries=countries,
        description=description
    )