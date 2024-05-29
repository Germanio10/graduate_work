import asyncio

import aiohttp
import pytest

from settings import test_settings


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

    async def inner(data: dict, method: str):
        url = f'{test_settings.assistant_service.url()}/{method}'
        async with aiohttp_client.post(url, json=data) as response:
            status = response.status
            body = await response.json()
            return {'body': body, 'status': status}

    return inner
