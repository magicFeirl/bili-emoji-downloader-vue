import os
from typing import Annotated

from contextlib import asynccontextmanager

import aiohttp
import uvicorn
import dotenv
from fastapi import FastAPI, Depends, Header
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


app = FastAPI(lifespan=lifespan, root_path='/api')

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

    # 没传或者传空 cookie，用环境变量的 cookie
    if (not kwargs.get('cookie')) and sessdata and bili_jct:
        cookie = f'SESSDATA={sessdata}; bili_jct={bili_jct}'
    else:
        cookie = kwargs.get('cookie', '')

    if isinstance(cookie, dict):
        cookie = '; '.join([f'{k}={v}' for k, v in cookie.items()])

    return aiohttp.ClientSession(headers={
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'cookie': cookie
    })


async def commonQuery(name: str, pn: int = 1, ps: int = 20, x_bili_cookie: Annotated[str | None, Header()] = None):
    return {'name': name, 'pn': pn, 'ps': ps, 'bili_cookie': x_bili_cookie}


CommonQuery = Annotated[dict, Depends(commonQuery)]


async def search_by_app(dep: CommonQuery):
    access_key, appkey = os.environ['access_key'], os.environ['appkey']
    url = f'https://api.bilibili.com/x/emote/package/search?access_key={access_key}&appkey={appkey}&business=reply&name={dep["name"]}'
    # vercel backend 似乎不能用全局变量保存 session
    async with get_session() as session:
        async with session.get(url, params={
            'business': 'reply',
            'pn': dep['pn'],
            'ps': dep['ps']
        }) as resp:
            return await resp.json()


async def search_by_pc(dep: CommonQuery):
    url = 'https://api.bilibili.com/bapis/main.community.interface.emote.EmoteService/AllPackages'

    cookie = dep.get('bili_cookie')
    cookie_dict = {}

    if cookie and isinstance(cookie, str):
        for k, v in [c.split('=') for c in cookie.split(';')]:
            cookie_dict[k.strip()] = v.strip()

    if not cookie_dict or 'SESSDATA' not in cookie_dict or 'bili_jct' not in cookie_dict:
        auth_method = 'env'
        cookie = {'bili_jct': os.environ['bili_jct'],
                  'SESSDATA': os.environ['sessdata']}
    else:
        auth_method = 'remote'
        cookie = {**cookie_dict}

    async with get_session(cookie=cookie) as session:
        resp = await session.get(url, params={
            'business': 'reply',
            'csrf': cookie.get('bili_jct'),
            'pn': dep['pn'],
            'ps': dep['ps'],
            'search': dep['name'],
        })

        return {**(await resp.json()), 'auth_method': auth_method}


async def search_by_pc_id(id: int | str):
    url = 'https://api.bilibili.com/bapis/main.community.interface.emote.EmoteService/PackageDetail'

    async with get_session() as session:
        resp = await session.get(url, params={
            'business': 'reply',
            'id': id
        })

        return await resp.json()


@app.get('/detail')
async def get_detail_by_id(id: int | str):
    if not os.environ['bili_jct'] or not os.environ['sessdata']:
        return {'code': -1, 'message': '该接口仅在配置 cookie 登录后可用'}

    return await search_by_pc_id(id)


@app.get('/index')
async def search(query: CommonQuery):
    access_key, appkey = os.environ.get('access_key'), os.environ.get('appkey')
    sessdata, bili_jct = os.environ.get('sessdata'), os.environ.get('bili_jct')

    if sessdata and bili_jct:
        return {**(await search_by_pc(query)), 'method': 'pc'}
    elif access_key and appkey:
        return {**(await search_by_app(query)), 'method': 'app'}
    else:
        return {'code': -1, 'message': '未配置登陆凭据，请在环境变量中配置 access_key 和 appkey(app登陆) 或者 sessdata 和 bili_jct(cookie)'}


if __name__ == '__main__':
    uvicorn.run('index:app', reload=True)
