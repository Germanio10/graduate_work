from functools import lru_cache
from http import HTTPStatus

from aiohttp import ClientResponse, ClientSession
from core.config import settings
from fastapi import Depends, HTTPException
from pydantic import BaseModel


class ApiResponse(BaseModel):
    status: int
    body: dict
    headers: dict


session: ClientSession | None = None


def get_api_session() -> ClientSession | None:
    return session


class ApiClient:
    def __init__(self, base_url: str, session: ClientSession):
        self.base_url = base_url
        self.session = session

    async def get(self, path, **kwargs) -> ClientResponse:
        url = f'{self.base_url}{path}'
        async with self.session.get(
            url,
            # cookies=cookies,
            params={**kwargs},
        ) as response:
            if response.status != HTTPStatus.OK:
                raise HTTPException(status_code=response.status)
            return await response.json()
