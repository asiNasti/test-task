from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.schemas.movie import MovieData


async def get_film_data(title: str):
    search_url = f"https://ua.kinorium.com/search/?q={title}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await page.goto(search_url, wait_until="domcontentloaded")

        try:
            film_url = await get_film_link(page)

            await page.goto(film_url, wait_until="networkidle")
            content = await page.content()

            soup = BeautifulSoup(content, "html.parser")
            data = get_data(soup, film_url)
            return data

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()


def get_data(soup: BeautifulSoup, url) -> MovieData:
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
        url=url,
        original_title=orig_title.get_text(strip=True) if orig_title else None,
        year=int(year.get_text(strip=True)) if year else None,
        slogan=slogan.get_text(strip=True).strip("«»").replace('\xa0', ' ') if slogan else None,
        rating_imdb=float(rating.get_text(strip=True)) if rating else None,
        genres=genres,
        countries=countries,
        description=description
    )

async def get_film_link(page):
    first_movie_locator = page.locator(".movieList .item a.search-page__title-link").first
    movie_id_path = await first_movie_locator.get_attribute("href")
    return  f"https://ua.kinorium.com{movie_id_path}"

if __name__ == "__main__":
    import asyncio
    import sys

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(get_film_data("Гра престолів"))