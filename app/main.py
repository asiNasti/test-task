from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from app.api.router import router


app = FastAPI(title="Kinorium Scraper")

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

app.include_router(router)
