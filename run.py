import asyncio
import sys
import uvicorn
from app.main import app
from app.core.config import settings


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    uvicorn.run(app, port=settings.port)
    