import asyncio
import uuid

import aiohttp
import pytest
from async_fastapi_jwt_auth import AuthJWT
from settings import JWTSettings, test_settings


@AuthJWT.load_config
def get_config():
    return JWTSettings()


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def aiohttp_client():
    client = aiohttp.ClientSession()
    yield client
    await client.close()


@pytest.fixture(scope='session')
def make_post_request(aiohttp_client):

    async def inner(data: dict, method: str, access_token: str = None):
        url = f'{test_settings.assistant_service.url()}/{method}'
        cookies = {}
        if access_token:
            cookies = {'access_token_cookie': access_token}
        async with aiohttp_client.post(url, json=data, cookies=cookies) as response:
            body = None
            status = response.status
            if (
                'Content-Type' in response.headers
                and 'application/json' in response.headers['Content-Type']
            ):
                body = await response.json()
            return {'body': body, 'status': status}

    return inner


@pytest.fixture(scope='session')
def get_token():

    async def inner(*args, **kwargs):
        return await AuthJWT().create_access_token(
            subject=str(uuid.uuid4()), user_claims={'role_id': str(uuid.uuid4())}
        )

    return inner
