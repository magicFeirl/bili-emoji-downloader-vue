import json
import os


from contextlib import asynccontextmanager

import aiohttp
import uvicorn
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

session: aiohttp.ClientSession = None

dotenv.load_dotenv()


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
    allow_origins=[
        'http://localhost:5173',
        'https://bili-emoji-downloader-vue.vercel.app'
    ]
)


def get_session():
    return aiohttp.ClientSession(headers={
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    })


@app.get('/api/index')
async def search(name: str, pn: int = 1, ps: int = 20):
    # with open('mock.json', 'r', encoding='utf-8') as f:
    #     return json.load(f)
    access_key, appkey = os.environ['access_key'], os.environ['appkey']
    url = f'https://api.bilibili.com/x/emote/package/search?access_key={access_key}&appkey={appkey}&business=reply&name={name}'
    # vercel backend 似乎不能用全局变量保存 session
    async with get_session() as session:
        async with session.get(url, params={
            'pn': pn,
            'ps': ps
        }) as resp:
            return await resp.json()


if __name__ == '__main__':
    uvicorn.run('index:app', reload=True)
