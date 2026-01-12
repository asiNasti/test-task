import httpx
from bs4 import BeautifulSoup

async def quick_test():
    #url = "https://ua.kinorium.com/101209/"
    url = "https://ua.kinorium.com/553240/"
    #url = "https://ua.kinorium.com/2106140/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    print(f"Loading: {url}...")
    
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url)
        
        # if error -> return
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            
            title = soup.select_one(".film-page__title-text")
            orig_title = soup.select_one(".film-page__orig_with_comment")
            year_el = soup.select_one(".film-page__nowrap-wrap_year a")
            
            #sep function 
            year = None
            if year_el:
                try:
                    year = int(year_el.get_text(strip=True))
                except ValueError:
                    year = None

            slogan_el = soup.select_one(".film-page__slogan")
            slogan = slogan_el.get_text(strip=True).strip("«»").replace('\xa0', ' ') if slogan_el else None

            rating = soup.select_one("ratingsBlockIMDb .value")
            
            # sep function
            '''
            rating = None
            if rating_el:
                try:
                    rating = float(rating_el.get_text(strip=True))
                except ValueError:
                    rating = None
            '''
            
            genres = [el.get_text(strip=True) for el in soup.find_all("li", itemprop="genre")]
            countries = [a.get_text(strip=True) for a in soup.select(".film-page__country-links a")]

            #sep function
            desc_el = soup.select_one(".film-page__text")
            if desc_el:
                if desc_el.h2:
                    desc_el.h2.decompose() 
                description = desc_el.get_text(strip=True).replace('\xa0', ' ')
            else:
                description = None

            # create struct
            print("-" * 30)
            print(f"Title: {title.get_text(strip=True) if title else 'No found'}")
            print(f"Original: {orig_title.get_text(strip=True) if orig_title else 'No found'}")
            print(f"Year: {year}")
            print(f"Slogan: {slogan}")
            print(f"Rating: {rating.get_text(strip=True) if rating else 'No found'}")
            print(f"genres: {genres}")
            print(f"countries: {countries}")
            print(f"description: {description}")
            print("-" * 30)
        else:
            print(f"Error: {response.status_code}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(quick_test())