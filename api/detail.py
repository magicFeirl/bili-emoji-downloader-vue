import os

from index import get_session, app
import aiohttp
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

session: aiohttp.ClientSession = None

dotenv.load_dotenv()


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
