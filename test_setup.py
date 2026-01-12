import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://ua.kinorium.com/553240/")
        print(f"Title: {await page.title()}")
        await asyncio.sleep(3)
        await browser.close()

asyncio.run(run())