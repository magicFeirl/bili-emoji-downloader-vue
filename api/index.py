import json
from contextlib import asynccontextmanager

import aiohttp
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config


session: aiohttp.ClientSession = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global session
    session = aiohttp.ClientSession(headers={
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    })
    yield
    await session.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


@app.get('/search')
async def search_emoji_pack(name: str, pn: int = 1, ps: int = 20):
    # with open('mock.json', 'r', encoding='utf-8') as f:
    #     return json.load(f)

    url = f'https://api.bilibili.com/x/emote/package/search?access_key={config.access_key}&appkey={config.appkey}&business=reply&name={name}'

    async with session.get(url, params={
        'pn': pn,
        'ps': ps
    }) as resp:
        return await resp.json()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)