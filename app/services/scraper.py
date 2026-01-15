import asyncio
from playwright.async_api import async_playwright
from app.core.config import settings


async def run_playwright(url: str, headless: bool = True, wait_selector: str = None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(user_agent=settings.user_agent)
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded")

            if "/search/" in page.url:
                await page.wait_for_selector(".search-page__title-link", timeout=5000)
                link = await get_film_link(page)
                await page.goto(link, wait_until="networkidle")

            if wait_selector:
                await page.wait_for_selector(wait_selector, timeout=settings.default_timeout)
            
            content = await page.content()
            final_url = page.url

            if not headless:
                await asyncio.sleep(settings.default_wait_time)
                
            return content, final_url
        
        except Exception as e:
            print(f"Scraping error: {e}")
            return None, url
        finally:
            await browser.close()


async def get_film_link(page):
    try:
        first_movie_locator = page.locator(".movieList .item a.search-page__title-link").first
        movie_id_path = await first_movie_locator.get_attribute("href")
        if movie_id_path:
            return f"{settings.kinorium_base_url}{movie_id_path}"
        
    except Exception:
        return None
    
    return None
