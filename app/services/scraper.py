import re
from bs4 import BeautifulSoup
import httpx
from playwright.async_api import async_playwright
from ..schemas.movie import MovieData, ScrapeMethod

class KinoriumScraper:
    def __init__(self, url: str):
        self.url = url

    def _parse_html(self, html: str) -> MovieData:
        soup = BeautifulSoup(html, "html.parser")

        title_el = soup.select_one("h1.film-page__title-text")
        title = title_el.get_text(strip=True) if title_el else "Not found"

        orig_title_el = soup.select_one("h2.film-page__orig_with_comment")
        orig_title = orig_title_el.get_text(strip=True) if orig_title_el else None

        year_el = soup.select_one(".film-page__nowrap-wrap_year a")
        year = None
        if year_el:
            try:
                year = int(year_el.get_text(strip=True))
            except ValueError:
                year = None

        slogan_el = soup.select_one(".film-page__slogan")
        slogan = slogan_el.get_text(strip=True).strip("«»").replace('\xa0', ' ') if slogan_el else None

        rating_el = soup.select_one("ratingsBlockIMDb .value")
        rating = None
        if rating_el:
            try:
                rating = float(rating_el.get_text(strip=True))
            except ValueError:
                rating = None

        genres = [el.get_text(strip=True) for el in soup.find_all("li", itemprop="genre")]

        countries = [a.get_text(strip=True) for a in soup.select(".film-page__country-links a")]

        desc_el = soup.select_one(".film-page__text")
        description = None
        if desc_el:
            if desc_el.h2:
                desc_el.h2.decompose() 
            description = desc_el.get_text(strip=True).replace('\xa0', ' ')


        return MovieData(
            title=title,
            url=self.url,
            original_title=orig_title,
            year=year,
            slogan=slogan,
            rating_imdb=rating,
            genres=genres,
            countries=countries,
            description=description
        )
    
    async def scrape_http(self) -> MovieData:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
            response = await client.get(self.url)
            
            if response.status_code == 200:
                return self._parse_html(response.text)
            else:
                raise Exception(f"Failed to fetch data: {response.status_code}")

    async def scrape_playwright(self, headless: bool) -> MovieData:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            page = await browser.new_page()
            await page.set_extra_http_headers(self.headers)
            
            await page.goto(self.url, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000) 
            
            content = await page.content()
            await browser.close()
            return self._parse_html(content)