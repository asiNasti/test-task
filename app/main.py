from fastapi import FastAPI

from app.api.router import router


app = FastAPI(title="Kinorium Scraper")

app.include_router(router)
