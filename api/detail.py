import os

import aiohttp
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

session: aiohttp.ClientSession = None

dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'https://bili-emoji-downloader-vue.vercel.app'
    ]
)


def get_session(**kwargs):
    sessdata, bili_jct = os.environ.get(
        'sessdata', ''), os.environ.get('bili_jct', '')

    if 'cookie' not in kwargs and sessdata and bili_jct:
        cookie = f'SESSDATA={sessdata}; bili_jct={bili_jct}'
    else:
        cookie = kwargs.get('cookie', '')

    return aiohttp.ClientSession(headers={
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'cookie': cookie
    })


async def search_by_pc_id(id: int | str):
    url = 'https://api.bilibili.com/bapis/main.community.interface.emote.EmoteService/PackageDetail'

    async with get_session() as session:
        resp = await session.get(url, params={
            'business': 'reply',
            'id': id
        })

        return await resp.json()


@app.get('/api/detail')
async def get_detail_by_id(id: int | str):
    if not os.environ['bili_jct'] or not os.environ['sessdata']:
        return {'code': -1, 'message': '该接口仅在配置 cookie 登录后可用'}

    return await search_by_pc_id(id)
