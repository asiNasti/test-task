from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.schemas.movie import MovieResponse


def create_new_url(url, genre_id):
    new_url = f"{url}&genres%5B%5D={genre_id}"
    return new_url

def get_data(soup: BeautifulSoup):
    films = soup.select('.filmList__item-wrap-title')
    print(films)
    films_data = []
    for film in films:
        title_el = film.select_one(".movie-title__text .title")
        link_el = film.select_one("a")
        
        if title_el and link_el:
            title = title_el.get_text(strip=True).replace('\xa0', ' ')
            url = "https://ua.kinorium.com" + link_el['href']
            films_data.append(MovieResponse(title=title, url=url))
    return films_data


async def get_film_data(genre_id):
    url = "https://ua.kinorium.com/R2D2/?order=rating&page=1&perpage=200"
    genre_url = create_new_url(url, genre_id)
    print(f"Loading: {genre_url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            await page.goto(genre_url)
            await page.wait_for_selector(".filmList", timeout=15000)
            content = await page.content()

            soup = BeautifulSoup(content, "html.parser")
            return get_data(soup)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
    



if __name__ == "__main__":
    import asyncio
    url = "https://ua.kinorium.com/R2D2/?order=rating&page=1&perpage=50"
    genre = 1
    asyncio.run(get_film_data(genre))