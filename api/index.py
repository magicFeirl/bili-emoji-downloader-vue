import os
from typing import Annotated, Optional

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


def get_session(dep):
    cookie, _ = get_cookie(dep)

    if isinstance(cookie, dict):
        cookie = '; '.join([f'{k}={v}' for k, v in cookie.items()])

    return aiohttp.ClientSession(headers={
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'cookie': cookie
    })


async def commonQuery(pn: int = 1, ps: int = 20, x_bili_cookie: Annotated[str | None, Header()] = None):
    return {'pn': pn, 'ps': ps, 'bili_cookie': x_bili_cookie}


CommonQuery = Annotated[dict, Depends(commonQuery)]


def get_cookie(dep: CommonQuery):
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

    return (cookie, auth_method)


async def basic_get(url: str, dep: CommonQuery, **kwargs):
    async with get_session(dep) as session:
        async with session.get(url, **kwargs) as resp:
            return {**await resp.json()}


async def search_by_app(name: str, dep: CommonQuery):
    access_key, appkey = os.environ['access_key'], os.environ['appkey']
    url = f'https://api.bilibili.com/x/emote/package/search?access_key={access_key}&appkey={appkey}&business=reply&name={name}'

    return await basic_get(url, dep, params={
        'business': 'reply',
        'pn': dep['pn'],
        'ps': dep['ps']
    })


async def search_by_pc(name: str, dep: CommonQuery):
    url = 'https://api.bilibili.com/bapis/main.community.interface.emote.EmoteService/AllPackages'

    cookie, _ = get_cookie(dep)

    return await basic_get(url, dep, params={
        'business': 'reply',
        'csrf': cookie.get('bili_jct'),
        'pn': dep['pn'],
        'ps': dep['ps'],
        'search': name,
    })


async def search_by_pc_id(id: int | str):
    url = 'https://api.bilibili.com/bapis/main.community.interface.emote.EmoteService/PackageDetail'

    return await basic_get(url, {}, params={
        'business': 'reply',
        'id': id
    })


@ app.get('/detail', description='通过 PC 端接口获取表情包详情')
async def get_detail_by_id(id: int | str):
    if not os.environ['bili_jct'] or not os.environ['sessdata']:
        return {'code': -1, 'message': '该接口仅在配置 cookie 登录后可用'}

    return await search_by_pc_id(id)


@ app.get('/collection')
async def search_collection(keyword: str, query: CommonQuery):
    url = 'https://api.bilibili.com/x/garb/v2/mall/home/search'

    query.pop('bili_cookie')

    return await basic_get(url, query, params={
        **query,
        'key_word': keyword
    })


@ app.get('/collection-detail')
async def collection_detail(act_id: int, lottery_id: int, query: CommonQuery):
    url = 'https://api.bilibili.com/x/vas/dlc_act/lottery/detail'

    return await basic_get(url, query,  params={
        'act_id': act_id,
        'lottery_id': lottery_id,
    })


@ app.get('/suit-detail')
async def suit_detail(item_id: int, query: CommonQuery):
    url = 'https://api.bilibili.com/x/garb/v2/mall/suit/detail'

    return await basic_get(url, query, params={
        'item_id': item_id,
        'part': 'suit',
    })


@ app.get('/index')
async def search(name: str, query: CommonQuery):
    access_key, appkey = os.environ.get('access_key'), os.environ.get('appkey')
    sessdata, bili_jct = os.environ.get('sessdata'), os.environ.get('bili_jct')

    if sessdata and bili_jct:
        return {**(await search_by_pc(name, query)), 'method': 'pc'}
    elif access_key and appkey:
        return {**(await search_by_app(query)), 'method': 'app'}
    else:
        return {'code': -1, 'message': '未配置登陆凭据，请在环境变量中配置 access_key 和 appkey(app登陆) 或者 sessdata 和 bili_jct(cookie)'}


if __name__ == '__main__':
    uvicorn.run('index:app', reload=True)
