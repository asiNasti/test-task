import asyncio
import sys
import uvicorn
from test_fastapi import app


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
    