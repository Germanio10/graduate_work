from contextlib import asynccontextmanager

import aiohttp
import uvicorn
from api.v1 import assistant
from db import api_client, redis
from fastapi import FastAPI
from redis.asyncio import Redis
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_client.session = aiohttp.ClientSession()
    redis.redis = Redis(host=settings.redis_settings.host, port=settings.redis_settings.port)

    yield

    await api_client.session.close()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    lifespan=lifespan,
)

app.include_router(assistant.assistant_route, prefix='/api/v1/assistant', tags=['assistant'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
